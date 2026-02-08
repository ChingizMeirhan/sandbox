from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.event import Event
from app.schemas.event import EventIn, EventOut

router = APIRouter()


@router.get("/healthz")
def healthz():
    # liveness: процесс жив, без проверок зависимостей
    return {"status": "ok"}


@router.get("/readyz")
def readyz(db: Session = Depends(get_db)):
    # readiness: сервис готов обслуживать запросы (БД доступна)
    try:
        db.execute(select(1))
    except Exception:
        raise HTTPException(status_code=503, detail="db_unavailable")
    return {"status": "ready"}


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
