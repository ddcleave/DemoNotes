from typing import Optional

from fastapi import HTTPException
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name,
                         auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        token: str = request.cookies.get("access_token")

        if not token:
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"
                )
            else:
                return None
        return token


class OAuth2RefreshToken(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name,
                         auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        token: str = request.cookies.get("refresh_token")

        if not token:
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                )
            else:
                return None
        return token
