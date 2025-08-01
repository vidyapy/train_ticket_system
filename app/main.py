from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError, StarletteHTTPException

from app.helpers.common import create_error_response, format_pydantic_error
from app.core.config import get_settings
from app.services.email_scheduler import start_scheduler
from app.api import api_v1
from app.core.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup initiated.")
    start_scheduler()
  
    yield 
    print("Application shutdown initiated.")
    await engine.dispose()
 
app = FastAPI(
    title="Train Ticket Booking System API",
    version="1.0.0",
    description="An API for managing train ticket bookings and related operations.",
    lifespan=lifespan,
    docs_url="/docs",      
    redoc_url="/redoc",    
    openapi_url="/openapi.json"
)

# Custom exception handlers
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return await create_error_response(exc, exc.status_code, exc.detail, request)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_message = format_pydantic_error(exc)
    return await create_error_response(exc, status.HTTP_422_UNPROCESSABLE_ENTITY, {"message": error_message}, request)

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    
    return await create_error_response(exc, status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error", request)


app.include_router(api_v1.api_router, prefix="/api/v1", tags=["v1"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Train Ticket Booking System API!"}
