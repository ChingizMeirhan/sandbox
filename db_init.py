from datetime import datetime
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine

DB_URL = "postgresql+psycopg://petuser:petpass@localhost:5432/petdb"

engine = create_engine(DB_URL, pool_pre_ping=True)


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(64), nullable=False)     # кто прислал
    type: Mapped[str] = mapped_column(String(64), nullable=False)       # тип события
    payload: Mapped[str] = mapped_column(Text, nullable=False)          # сырой payload (позже сделаем JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


def main() -> None:
    Base.metadata.create_all(engine)
    print("OK: tables created/verified")


if __name__ == "__main__":
    main()
