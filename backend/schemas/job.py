from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class TicketJobResponse(BaseModel):
    """Response when checking job status"""

    job_id: str
    source: str
    status: str  # "pending", "processing", "completed", "failed"
    tickets_found: Optional[int]
    error: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True
