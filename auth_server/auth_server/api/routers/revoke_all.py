from auth_server.api.dependencies.tokens import delete_all_refresh_tokens
from auth_server.api.dependencies.get_user import get_user
from fastapi import APIRouter, Depends
from auth_server.models import ResponseAuth


router = APIRouter()


@router.post("/revoke_all", response_model=ResponseAuth)
async def revoke_all_refresh_tokens(user: str = Depends(get_user)):
    delete_all_refresh_tokens(user)
    return {"operation": "revoke_all", "successful": True}
