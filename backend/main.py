from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from routers import ticket
from db.database import create_tables

import os

db_path = settings.DATABASE_URL.replace("sqlite:///", "")
full_path = os.path.abspath(db_path)
print(f"📂 FastAPI using database: {full_path}")

create_tables()

app = FastAPI(
    title="Tix",
    description="get the best ticket deals",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ticket.router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
