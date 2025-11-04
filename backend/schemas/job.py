from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class JobResponse(BaseModel):
    """Response when checking job status"""

    id: int
    job_type: str
    source: str
    source_id: Optional[str]
    status: str  # "pending", "processing", "completed", "failed"
    tickets_found: Optional[int]
    tickets_analyzed: Optional[int]
    error: Optional[str]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class CreateJobRequest(BaseModel):
    """
    What frontend sends to start a new job
    Example: POST /api/jobs {"source": "reddit", "source_id": "1nvaldi"}
    """

    source: str  # "reddit", "craigslist"
    source_id: Optional[str] = None  # Reddit post ID, etc.


class JobStatusResponse(BaseModel):
    """Quick status check response"""

    job_id: int
    status: str
    progress: Optional[str] = None  # "Found 15 tickets, analyzed 12"
