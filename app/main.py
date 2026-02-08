from fastapi import FastAPI

from app.api.routes import router
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title="Events Journal", version="0.1.0")
app.include_router(router)


@app.on_event("startup")
def startup() -> None:
    # MVP-режим: позже заменим на Alembic миграции
    Base.metadata.create_all(engine)
