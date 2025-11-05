from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.models.job import TicketJob
from backend.schemas.job import TicketJobResponse

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)


@router.get("/{job_id}", response_model=TicketJobResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(TicketJob).filter(TicketJob.job_id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job
