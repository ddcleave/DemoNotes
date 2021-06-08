from fastapi import APIRouter, Depends
from src.dependencies import get_user


router = APIRouter()

# /note/id/export
# post - create_sharing_token
# delete - delete_sharing_token
# get - получить код

@router.post("/note/{id}/export")
def create_sharing_token(id: str, user: str = Depends(get_user)):
    pass

@router.delete("/note/{id}/export")
def delete_sharing_token(id: str, user: str = Depends(get_user)):
    pass

@router.get("/note/{id}/export")
def get_sharing_token(id: str):
    pass
