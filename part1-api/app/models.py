import uuid
from sqlalchemy import Column, String, DateTime, text,func
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

class Clan(Base):
    __tablename__ = "clans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    region = Column(String, nullable=True)
    '''
    created_at = Column(
    DateTime(timezone=True),
    server_default=func.now(),  # works in both Postgres and SQLite
    nullable=False,
    )
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=text("(now() at time zone 'utc')"),
        nullable=False,
    )
    '''
