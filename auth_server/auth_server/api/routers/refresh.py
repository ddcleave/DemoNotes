import json

from auth_server.api.dependencies.authentiction import oauth2_refresh_scheme
from auth_server.api.dependencies.tokens import create_and_set_tokens
from auth_server.core.config import Settings, get_settings
from auth_server.db.redis import redis_db
from auth_server.models import ResponseAuth
from fastapi import (APIRouter, Depends, Form, HTTPException, Request,
                     Response, status)

router = APIRouter()


@router.post("/refresh", response_model=ResponseAuth)
async def refresh_token_for_access_token(
        response: Response,
        request: Request,
        fingerprint: str = Form(...),
        refresh_token: str = Depends(oauth2_refresh_scheme),
        settings: Settings = Depends(get_settings)
):
    refresh_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )
    if refresh_token is None:
        raise refresh_exception

    namespace = "r_token:"
    with redis_db.pipeline() as pipe:
        pipe.multi()
        pipe.get(namespace + refresh_token)
        pipe.delete(namespace + refresh_token)
        result = pipe.execute()

    if result[1] == 0:
        raise refresh_exception
    if not result[0]:
        raise refresh_exception

    token_info = json.loads(result[0])

    if token_info["fingerprint"] != fingerprint:
        raise refresh_exception

    ip = request.client.host
    if token_info["ip"] != ip:
        raise refresh_exception

    username = token_info["username"]
    # user_result = await database.fetch_one(get_user_from_db(username))
    # if not user_result:
    #     raise refresh_exception
    await create_and_set_tokens(username, fingerprint,
                                ip, response, settings)
    return {"operation": "refresh", "successful": True}
