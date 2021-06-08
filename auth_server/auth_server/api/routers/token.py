from auth_server.api.dependencies.authentiction import authenticate_user
from auth_server.api.dependencies.tokens import create_and_set_tokens
from auth_server.core.config import Settings, get_settings
from auth_server.models import ResponseAuth
from fastapi import (APIRouter, Depends, HTTPException, Request, Response,
                     status)
from auth_server.api.dependencies.forms import PasswordRequestForm

router = APIRouter()


@router.post("/token", response_model=ResponseAuth)
async def login_for_access_token(
    response: Response,
    request: Request,
    form_data: PasswordRequestForm = Depends(),
    settings: Settings = Depends(get_settings)
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    await create_and_set_tokens(user.username, form_data.fingerprint,
                                request.client.host, response, settings)
    return {"operation": "login", "successful": True}
