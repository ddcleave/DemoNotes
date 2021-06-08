from auth_server.api.dependencies.get_userdata_from_token import \
    get_userdata_from_registration_token
from auth_server.api.dependencies.queries_to_db import create_new_user
from fastapi import APIRouter, Depends


router = APIRouter()


@router.post("/verify")
async def email_verification(
    userdata: dict = Depends(get_userdata_from_registration_token)
):
    await create_new_user(userdata["username"], userdata["fullname"],
                          userdata["email"], userdata["hash_password"])
    return {"username": userdata["username"]}
