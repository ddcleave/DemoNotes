from fastapi import APIRouter, Depends
from src.dependencies import get_user

router = APIRouter()

@router.get("/check")
async def get_username(user = Depends(get_user)):
    return {"username": user}

