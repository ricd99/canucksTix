import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session
import sys

sys.path.insert(1, "C://Users//ryanh//code//projects//canucksTix")

from backend.db.database import get_db, SessionLocal
from backend.models.ticket import Ticket
from backend.models.job import TicketJob
from backend.schemas.ticket import TicketResponse, TicketListResponse
from backend.schemas.job import TicketJobResponse


router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
)


@router.get("", response_model=TicketListResponse)
def get_tickets(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    return {"total": len(tickets), "tickets": tickets}
