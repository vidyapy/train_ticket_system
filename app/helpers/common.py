from typing import Any
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from fastapi import Request
from fastapi.responses import JSONResponse

import re
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from sqlalchemy.future import select
from app.models.user import User


def serialize_result(result: Any):
    if isinstance(result, BaseModel):
        return result.model_dump()  # Serialize BaseModel instances
    elif isinstance(result, list):
        # Handle list of BaseModel instances
        return [r.model_dump() if isinstance(r, BaseModel) else r for r in result]
    elif isinstance(result, dict):
        return {k: v for k, v in result.items()}  # Serialize dictionary
    else:
        return result  # Ensure other types are converted to string


def create_response(status: int, message: str, result: Any = None):
    response_result = serialize_result(result)
    
    return {
        "status": status,
        "message": message,
        "result": response_result if response_result is not None else []
    }


def format_pydantic_error(exc: RequestValidationError):
    formatted_errors = {}

    snake_case_pattern = re.compile(r"^[a-z_][a-z0-9_]*$")

    if isinstance(exc.errors(), str):
        return exc.errors()
    
    for err in exc.errors():
        loc = err.get('loc', [])
        field = "error"
        if len(loc) > 1 and isinstance(loc[-1], str) and snake_case_pattern.match(loc[-1]):
            field = loc[-1]
        formatted_errors[field] = err.get('msg', '')
    
    return formatted_errors


async def create_error_response(exc, status_code, message, request: Request):

    if isinstance(message, dict):
        # Use "message" field if it exists and serialize the rest into "result"
        response_message = message.pop("message", "An error occurred")
        response_result = serialize_result(message)
    else:
        # Message is a string, so result will be empty
        response_message = message
        response_result = None

    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "message": response_message,
            "result": response_result  # Serialized result
        },
    )


async def get_user_by_id(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).where(
        User.id == user_id,
        User.is_deleted == False
        ))
    return result.scalar_one_or_none()


def is_tatkal_window_open(departure_time: datetime, now: datetime = None) -> bool:
    if now is None:
        now = datetime.utcnow()
    tatkal_start = departure_time - timedelta(hours=2)
    tatkal_end = tatkal_start + timedelta(minutes=10)
    return tatkal_start <= now <= tatkal_end