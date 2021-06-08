from fastapi import APIRouter, Depends
from src.dependencies import get_user

router = APIRouter()
# /share/token
# get - get_sharing_note

# /share/token/import
# post - import_note

@router.get("/share/{token}")
def get_sharing_note(token: str, user: str = Depends(get_user)):
    pass

@router.post("/share/{token}/import")
def import_note(token: str, user: str = Depends(get_user)):
    pass