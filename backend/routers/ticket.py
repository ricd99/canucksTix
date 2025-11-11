import uuid
from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session
import sys

sys.path.insert(1, "C://Users//ryanh//code//projects//canucksTix")

from backend.db.database import get_db
from backend.models.ticket import Ticket
from backend.schemas.ticket import TicketResponse


router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
)


@router.get("", response_model=List[TicketResponse])
def get_tickets(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    print(f"📊 Found {len(tickets)} tickets in database")
    for ticket in tickets[:3]:  # Print first 3
        print(f"  - {ticket.id}: {ticket.author}")
    return tickets
