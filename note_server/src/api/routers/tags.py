from src.services.usecases import GetTags
from src.entities.note import TagsGet
from fastapi import APIRouter, Depends
from src.dependencies import get_user
from src.services.usecases import BaseUseCase
from src.services.adapters.postgres_storage import PostgresStorage

router = APIRouter()
# get - get_tags


def get_tags_usecase() -> BaseUseCase:
    return GetTags(PostgresStorage())


@router.get("/tags")
def get_tags(user: str = Depends(get_user),
             usecase = Depends(get_tags_usecase)):
    to_get_tags = TagsGet(user=user)
    return usecase.execute(to_get_tags)