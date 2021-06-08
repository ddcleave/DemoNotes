from uuid import UUID

from fastapi import APIRouter, Depends, Form
from src.dependencies import get_user
from src.entities.note import NoteCreate, NoteDelete, NoteGetItem, NoteUpdate
from src.schemas.requests import NewNote
from src.services.adapters.postgres_storage import PostgresStorage
from src.services.usecases import (BaseUseCase, CreateNote, DeleteNote,
                                   GetNote, UpdateNote)

router = APIRouter()

def create_note_usecase() -> BaseUseCase:
    return CreateNote(PostgresStorage())

def delete_note_usecase() -> BaseUseCase:
    return DeleteNote(PostgresStorage())

def update_note_usecase() -> BaseUseCase:
    return UpdateNote(PostgresStorage())

def get_note_usecase() -> BaseUseCase:
    return GetNote(PostgresStorage())


@router.post("/note/create")
def create_note(new_note: NewNote,   # надо сделать валидацию
                user: str = Depends(get_user),
                usecase = Depends(create_note_usecase)):
    note_for_create = NoteCreate(creator=user, data=new_note.note, tags=new_note.tags)
    return usecase.execute(note=note_for_create)

@router.get("/note/{id}")
def get_note(id: str, user: str = Depends(get_user),
             usecase = Depends(get_note_usecase)):
    find_note = NoteGetItem(user=user, id=id)
    return usecase.execute(note=find_note)

@router.put("/note/{id}")
def update_note(id: str, note: str = Form(...), user: str = Depends(get_user),
                usecase = Depends(update_note_usecase)):
    note_for_update = NoteUpdate(user=user, id=UUID(id), data=note)
    return usecase.execute(note=note_for_update)


@router.delete("/note/{id}")
def delete_note(id: str,
                user: str = Depends(get_user),
                usecase = Depends(delete_note_usecase)):
    note_for_delete = NoteDelete(id=UUID(id), user=user)
    return usecase.execute(note=note_for_delete)

@router.post("/note/swap/{first_id}/{second_id}")
def swap_notes(first_id: str, second_id: str, user: str = Depends(get_user)):
    pass


@router.post("/note/{id}/tag")
def add_tag(id: str, user: str = Depends(get_user)):
    pass

@router.delete("/note/{id}/tag")
def remove_tag(id: str, user: str = Depends(get_user)):
    pass
