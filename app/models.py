from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from sqlalchemy.sql import func
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, unique=True, index=True)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    source = Column(String, default="jsonplaceholder")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
