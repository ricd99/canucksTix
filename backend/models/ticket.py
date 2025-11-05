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
from sqlalchemy.orm import relationship

from db.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)  # "reddit", "craigslist", etc.
    author = Column(String)
    body = Column(String)
    created = Column(DateTime)
    permalink = Column(String)

    location = Column(String, nullable=True)
    price_per_ticket = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=True)
    game = Column(String, nullable=True)
    rating = Column(String, nullable=True)
    description = Column(String, nullable=True)
