from src.api.routers import (note, notes, check, tags, tag)
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(note.router, tags=["note"])
api_router.include_router(notes.router, tags=["notes"])
api_router.include_router(check.router, tags=["check"])
api_router.include_router(tags.router, tags=["tags"])
api_router.include_router(tag.router, tags=["tag"])
