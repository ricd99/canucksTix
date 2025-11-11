from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel


class TicketResponse(BaseModel):
    id: int
    source: str
    author: str
    body: str
    created: datetime
    permalink: str

    location: Optional[str]
    price_per_ticket: Optional[float]
    quantity: Optional[int]
    game: Optional[str]
    rating: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True
