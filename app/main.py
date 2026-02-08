from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.middleware import RequestIdMiddleware

setup_logging(settings.LOG_LEVEL)

app = FastAPI(title="Events Journal", version="0.1.0")

app.add_middleware(RequestIdMiddleware)
app.include_router(router)
