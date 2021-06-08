from typing import Optional
from src.entities.note import NoteFilter
from fastapi import APIRouter, Depends
from src.dependencies import get_user
from src.services.usecases import GetNotes, BaseUseCase
from src.services.adapters.postgres_storage import PostgresStorage

router = APIRouter()
# get - get_notes


def get_notes_usecase() -> BaseUseCase:
    return GetNotes(PostgresStorage())


@router.get("/notes")
def get_notes(position: Optional[int] = None,
              tag: Optional[str] = None,
              user: str = Depends(get_user),
              usecase = Depends(get_notes_usecase)):
    filter = NoteFilter(user=user, position=position, tag=tag)
    return usecase.execute(filter)
