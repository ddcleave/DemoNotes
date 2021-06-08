import uuid
from typing import Any, Optional
from datetime import datetime

from sqlalchemy.sql.sqltypes import Boolean, Integer, String
from src.db.models import Base
from pydantic import BaseModel
from uuid import UUID

class NoteCreate(BaseModel):
    creator: str
    data: str
    tags: list[str] = []


class TagAdd(BaseModel):
    pers_note_id: UUID
    user: str
    label: str


class TagCreate(BaseModel):
    label: str
    user: str


class NoteGetItem(BaseModel):
    user: str
    id: UUID


class TagItem(BaseModel):
    label: str

    class Config:
        orm_mode = True


class NoteDataItem(BaseModel):
    data: str
    create_date: datetime
    creator: str
    token: Optional[str] = None

    class Config:
        orm_mode = True


class NoteItem(BaseModel):
    id: UUID
    user: str
    shared: bool
    note: Optional[NoteDataItem]
    position: int
    tags: list[TagItem] = None

    class Config:
        orm_mode = True


class NoteUpdate(BaseModel):
    user: str
    id: UUID
    data: str


class NoteDelete(BaseModel):
    user: str
    id: UUID

class TagRemove(BaseModel):
    label: str
    user: str
    note_id: UUID


class NoteFilter(BaseModel):
    user: str
    position: Optional[int] = None
    tag: Optional[str] = None


class NoteSwapPosition(BaseModel):
    user: str
    first_note_id: UUID
    second_note_id: UUID

class NoteSetToken(BaseModel):
    user: str
    id: UUID


class NoteImportToken(BaseModel):
    user: str
    token: str

class NoteDeleteToken(BaseModel):
    user: str
    id: UUID

class NoteUUID(BaseModel):
    id: Optional[UUID]

class TagsGet(BaseModel):
    user: str