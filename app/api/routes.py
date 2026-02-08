from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.event import Event
from app.schemas.event import EventIn, EventOut

router = APIRouter()


@router.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(select(1))
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"db_unavailable: {type(e).__name__}")
    return {"status": "ok"}


@router.post("/events", response_model=EventOut, status_code=201)
def create_event(body: EventIn, db: Session = Depends(get_db)):
    ev = Event(source=body.source, type=body.type, payload=body.payload)
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev


@router.get("/events", response_model=list[EventOut])
def list_events(
    limit: int = Query(default=20, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return db.execute(
        select(Event).order_by(Event.id.desc()).limit(limit)
    ).scalars().all()
