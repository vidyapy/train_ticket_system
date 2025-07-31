from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import api_v1
from app.db.base import Base
from app.core.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: Close database connections
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(api_v1.api_router, prefix="/api/v1", tags=["v1"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Train Ticket Booking System API!"}
