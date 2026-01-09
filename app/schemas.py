from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostCreate(BaseModel):
    external_post_id: int

class PostUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    class Config:
        from_attributes = True

class PostRead(BaseModel):
    id: int
    external_id: int
    title: str
    body: str
    source: str
    created_at: datetime
    updated_at: datetime | None
