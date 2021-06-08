from auth_server.api.dependencies.authentiction import oauth2_refresh_scheme
from auth_server.api.dependencies.get_user import get_user
from auth_server.api.dependencies.tokens import invalidate_tokens
from auth_server.models import ResponseAuth
from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from auth_server.core.config import Settings, get_settings

router = APIRouter()


@router.post("/logout", response_model=ResponseAuth)
async def logout(
    response: Response,
    user: str = Depends(get_user),
    refresh_token: str = Depends(oauth2_refresh_scheme),
    settings: Settings = Depends(get_settings)
):
    content = {"operation": "logout", "successful": True}
    response = JSONResponse(content=content)
    invalidate_tokens(user, refresh_token, response, settings)
    return response
