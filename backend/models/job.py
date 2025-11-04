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
    job_type = Column(
        String, nullable=False
    )  # "reddit_scrape", "craigslist_scrape", etc.
    source = Column(String, nullable=False)  # "reddit", "craigslist", "marketplace"
    source_id = Column(String, nullable=True)  # Reddit post ID, Craigslist URL, etc.

    status = Column(
        String, default="pending"
    )  # "pending", "processing", "completed", "failed"
    tickets_found = Column(Integer, nullable=True)  # How many tickets found
    tickets_analyzed = Column(Integer, nullable=True)  # How many passed analysis

    error = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
