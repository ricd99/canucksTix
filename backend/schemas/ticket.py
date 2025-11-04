from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel

# id = Column(Integer, primary_key=True, index=True)
#     source = Column(String)  # "reddit", "craigslist", etc.
#     author = Column(String)
#     body = Column(String)
#     created = Column(DateTime)
#     permalink = Column(String)

#     location = Column(String, nullable=True)
#     price_per_ticket = Column(Float, nullable=True)
#     quantity = Column(Integer, nullable=True)
#     game = Column(String, nullable=True)
#     rating = Column(String, nullable=True)
#     description = Column(String, nullable=True)


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


class TicketListResponse(BaseModel):
    """
    Response when getting multiple tickets
    """

    total: int
    tickets: list[TicketResponse]
