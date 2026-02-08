import os
from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import String, Text, DateTime, func, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

DB_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://petuser:petpass@localhost:5432/petdb")
engine = create_engine(DB_URL, pool_pre_ping=True)


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(64), nullable=False)
    type: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class EventIn(BaseModel):
    source: str = Field(..., min_length=1, max_length=64)
    type: str = Field(..., min_length=1, max_length=64)
    payload: str = Field(..., min_length=1)


class EventOut(BaseModel):
    id: int
    source: str
    type: str
    payload: str
    created_at: datetime


app = FastAPI(title="Events Journal", version="0.1.0")


@app.on_event("startup")
def startup() -> None:
    # гарантируем, что таблица существует
    Base.metadata.create_all(engine)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/events", response_model=EventOut)
def create_event(body: EventIn):
    with Session(engine) as s:
        e = Event(source=body.source, type=body.type, payload=body.payload)
        s.add(e)
        s.commit()
        s.refresh(e)
        return EventOut(id=e.id, source=e.source, type=e.type, payload=e.payload, created_at=e.created_at)


@app.get("/events", response_model=List[EventOut])
def list_events(limit: int = 20):
    if limit < 1 or limit > 200:
        raise HTTPException(status_code=400, detail="limit must be 1..200")

    with Session(engine) as s:
        rows = s.execute(select(Event).order_by(Event.id.desc()).limit(limit)).scalars().all()
        return [
            EventOut(id=r.id, source=r.source, type=r.type, payload=r.payload, created_at=r.created_at)
            for r in rows
        ]
