from fastapi import APIRouter, Depends
from fastapi.param_functions import Form
from src.dependencies import get_user
from src.entities.note import TagAdd, TagCreate, TagRemove
from src.schemas.requests import UpdateTag
from src.services.adapters.postgres_storage import PostgresStorage
from src.services.usecases import AddTag, BaseUseCase, CreateTag, RemoveTag

router = APIRouter()
# /tag/create
# post - create_tag

# /tag/label
# get - вернуть запрос с заметками по этому тегу
# delete - delete_tag

def create_tag_usecase() -> BaseUseCase:
    return CreateTag(PostgresStorage())

def add_tag_usecase() -> BaseUseCase:
    return AddTag(PostgresStorage())

def remove_tag_usecase() -> BaseUseCase:
    return RemoveTag(PostgresStorage())

@router.post("/tag/create")
def create_tag(tag: str = Form(...),
               user: str = Depends(get_user),
               usecase = Depends(create_tag_usecase)):
    tag_for_create = TagCreate(user=user, label=tag)
    return usecase.execute(tag_for_create)



@router.post("/tag/add")
def add_tag_to_note(tag: UpdateTag,
                    user: str = Depends(get_user),
                    usecase = Depends(add_tag_usecase)):
    add_tag = TagAdd(pers_note_id = tag.note, user=user, label=tag.tag)
    return usecase.execute(add_tag)

@router.post("/tag/remove")
def remove_tag_from_note(tag: UpdateTag,
                         user: str = Depends(get_user),
                         usecase = Depends(remove_tag_usecase)):
    remove_tag = TagRemove(note_id = tag.note, user=user, label=tag.tag)
    return usecase.execute(remove_tag)

# @router.get("/tag/{label}")
# def get_tagged_notes(label: str, user: str = Depends(get_user)):
#     pass


# @router.delete("/tag/{label}")
# def delete_tag(label: str, user: str = Depends(get_user)):
#     pass
