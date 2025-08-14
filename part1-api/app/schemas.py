from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class ClanCreate(BaseModel):
    name: str = Field(..., min_length=1)
    region: Optional[str] = None

class ClanOut(BaseModel):
    id: UUID
    name: str
    region: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True