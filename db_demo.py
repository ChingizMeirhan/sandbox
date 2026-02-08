from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, func
from datetime import datetime

DB_URL = "postgresql+psycopg://petuser:petpass@localhost:5432/petdb"
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


def main() -> None:
    with Session(engine) as s:
        e = Event(source="manual", type="test", payload='{"hello":"world"}')
        s.add(e)
        s.commit()

        row = s.execute(select(Event).order_by(Event.id.desc()).limit(1)).scalar_one()
        print("Last event:", row.id, row.source, row.type, row.payload)


if __name__ == "__main__":
    main()
