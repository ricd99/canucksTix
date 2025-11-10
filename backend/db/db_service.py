from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import sys

# debugging purposes
import json

sys.path.insert(1, "C://Users//ryanh//code//projects//canucksTix")
from backend.models.ticket import Ticket
from backend.db.database import get_db


def _parse_created(value: Optional[str]):
    if value is None:
        return None
    try:
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value)
        if isinstance(value, str) and value.isdigit():
            return datetime.fromtimestamp(int(value))
        return datetime.fromisoformat(value)
    except Exception:
        # last-resort: return None so DB can handle or validation layer can catch
        return None


def get_ticket_by_permalink(db: Session, permalink: str) -> Optional[Ticket]:
    if not permalink:
        return None
    return db.query(Ticket).filter(Ticket.permalink == permalink).first()


def create_ticket(db: Session, ticket_data: Dict) -> Ticket:
    ticket = Ticket(
        source=ticket_data.get("source"),
        author=ticket_data.get("author"),
        body=ticket_data.get("body"),
        created=_parse_created(ticket_data.get("created")),
        permalink=ticket_data.get("permalink"),
        location=ticket_data.get("location"),
        price_per_ticket=ticket_data.get("price_per_ticket"),
        quantity=ticket_data.get("quantity"),
        game=ticket_data.get("game"),
        rating=ticket_data.get("rating"),
        description=ticket_data.get("description"),
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def create_ticket_batch(db: Session, tickets_data: List[Dict]) -> List[Ticket]:
    tickets = []
    for ticket_data in tickets_data:
        ticket = Ticket(
            source=ticket_data.get("source"),
            author=ticket_data.get("author"),
            body=ticket_data.get("body"),
            created=_parse_created(ticket_data.get("created")),
            permalink=ticket_data.get("permalink"),
            location=ticket_data.get("location"),
            price_per_ticket=ticket_data.get("price_per_ticket"),
            quantity=ticket_data.get("quantity"),
            game=ticket_data.get("game"),
            rating=ticket_data.get("rating"),
            description=ticket_data.get("description"),
        )
        tickets.append(ticket)
        db.add(ticket)
    db.commit()
    for ticket in tickets:
        db.refresh(ticket)
    return tickets


def upsert_ticket(db: Session, ticket_data: Dict) -> Ticket:
    """
    Update existing ticket if permalink matches, otherwise create.
    Overwrites fields present in ticket_data.
    """
    permalink = ticket_data.get("permalink")
    existing = get_ticket_by_permalink(db, permalink)
    if existing:
        # update fields
        for key, value in {
            "source": ticket_data.get("source"),
            "author": ticket_data.get("author"),
            "body": ticket_data.get("body"),
            "created": _parse_created(ticket_data.get("created")),
            "location": ticket_data.get("location"),
            "price_per_ticket": ticket_data.get("price_per_ticket"),
            "quantity": ticket_data.get("quantity"),
            "game": ticket_data.get("game"),
            "rating": ticket_data.get("rating"),
            "description": ticket_data.get("description"),
        }.items():
            if value is not None:
                setattr(existing, key, value)
        db.add(existing)
        # do not commit here for batch performance
        return existing
    else:
        # create new
        return Ticket(
            source=ticket_data.get("source"),
            author=ticket_data.get("author"),
            body=ticket_data.get("body"),
            created=_parse_created(ticket_data.get("created")),
            permalink=permalink,
            location=ticket_data.get("location"),
            price_per_ticket=ticket_data.get("price_per_ticket"),
            quantity=ticket_data.get("quantity"),
            game=ticket_data.get("game"),
            rating=ticket_data.get("rating"),
            description=ticket_data.get("description"),
        )


def upsert_ticket_batch(db: Session, tickets: List[Dict]) -> List[Ticket]:
    """
    For each ticket_data: if permalink exists, update; otherwise create.
    Commits once at the end and refreshes returned objects.
    """
    results: List[Ticket] = []

    for k, v in tickets.items():
        data_with_source = {"source": "reddit", **v}
        # print(json.dumps(data_with_source, indent=2))
        obj = upsert_ticket(db, data_with_source)
        if isinstance(obj, Ticket) and obj.id is None:
            # newly created object (not yet in DB) -> add to session
            db.add(obj)
        results.append(obj)

    db.commit()

    # refresh all results that are in session
    for r in results:
        try:
            db.refresh(r)
        except Exception:
            # object might not be in session if something went wrong; ignore refresh errors
            pass

    return results
