from auth_server.api.routers import (logout, refresh, reset_password,
                                     revoke_all, set_password, signup, token,
                                     verify)
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(refresh.router, tags=["refresh"])
api_router.include_router(signup.router, tags=["signup"])
api_router.include_router(token.router, tags=["token"])
api_router.include_router(verify.router, tags=["verify"])
api_router.include_router(revoke_all.router, tags=["revoke_all"])
api_router.include_router(reset_password.router, tags=["reset_password"])
api_router.include_router(set_password.router, tags=["set_password"])
api_router.include_router(logout.router, tags=["logout"])
