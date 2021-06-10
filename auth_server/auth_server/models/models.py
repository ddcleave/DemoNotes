from pydantic.networks import EmailStr
from auth_server.api.dependencies.queries_to_redis import exist_email, exist_username
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator


class User(BaseModel):
    user_id: int
    username: str
    full_name: str
    email: str


class UserInDB(User):
    hashed_password: str


class RefreshToken(BaseModel):
    refresh_token: UUID
    user_id: int
    fingerprint: str
    created_at: datetime
    expired_at: datetime
    unused: bool


class ResponseAuth(BaseModel):
    operation: str
    successful: bool


class TokenData(BaseModel):
    username: Optional[str] = None


class UsernameAndExist(BaseModel):
    username: str
    exist_username: bool


class EmailAndExist(BaseModel):
    email: str
    exist_email: bool


class UniqueUsernameAndEmail(BaseModel):
    username: UsernameAndExist
    email: EmailAndExist

    @validator("username")
    def username_validation(cls, v: str):
        if v.exist_username:
            raise ValueError('Username already exists')
        if exist_username(v.username) != 0:
            raise ValueError('Username already exists')
        return v

    @validator("email")
    def email_validation(cls, v: str):
        if v.exist_email:
            raise ValueError('email already exists')
        if exist_email(v.email) != 0:
            raise ValueError('Email already exists')
        return v


class EmailRequest(BaseModel):
    email: EmailStr
