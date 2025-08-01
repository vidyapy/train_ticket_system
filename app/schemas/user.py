from pydantic import BaseModel, validator
from uuid import UUID

from app.helpers.validators import (
    validate_username, 
    validate_email, 
    validate_password
)


class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str
    is_admin: bool = False

    @validator("email")
    def check_email(cls, v):
        return validate_email(v)
    
    @validator("username")
    def check_username(cls, v):
        return validate_username(v)
    
    @validator("password")
    def check_password(cls, v):
        return validate_password(v)


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    is_admin: bool
    is_active: bool
    is_deleted: bool

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    username: str
    password: str

    @validator("username")
    def check_username(cls, v):
        return validate_username(v)
    
    @validator("password")
    def check_password(cls, v):
        return validate_password(v)
    
class LoginResponse(BaseModel):
    user_id: UUID
    access_token: str
    refresh_token: str

    class Config:
        orm_mode = True
