from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, ConfigDict, field_validator


class EventIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str = Field(..., min_length=1, max_length=64)
    type: str = Field(..., min_length=1, max_length=64)
    payload: dict[str, Any]

    @field_validator("source", "type")
    @classmethod
    def normalize_text(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be empty")
        return v


class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source: str
    type: str
    payload: dict[str, Any]
    created_at: datetime
