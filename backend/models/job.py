from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Boolean,
    ForeignKey,
    JSON,
)
from sqlalchemy.sql import func

from db.database import Base


class TicketJob(Base):
    __tablename__ = "ticket_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True, unique=True)
    source = Column(String, nullable=False)  # "reddit", "craigslist", "marketplace"

    status = Column(
        String, default="pending"
    )  # "pending", "processing", "completed", "failed"
    tickets_found = Column(Integer, nullable=True)  # How many tickets found

    error = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
