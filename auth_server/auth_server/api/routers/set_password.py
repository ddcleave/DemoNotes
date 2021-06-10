# вытаскиваем токен из ссылки, проверяем его валидность
# получаем новый пароль
# сбрасываем все рефреш токены
# устанавливаем новый пароль
from auth_server.api.dependencies.get_userdata_from_token import \
    get_email_from_restore_token
from auth_server.api.dependencies.queries_to_db import (
    get_userdata_from_email, replace_password)
from auth_server.api.dependencies.tokens import delete_all_refresh_tokens
from auth_server.services.password import get_password_hash
from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from pydantic.class_validators import validator
from pydantic.error_wrappers import ValidationError
from pydantic.main import BaseModel
from pydantic.networks import EmailStr

router = APIRouter()


class UpdataUserData(BaseModel):
    username: str
    password: str


class DataFromUser(BaseModel):
    username_from_db: str
    username: str

    @validator("username")
    def username_validation(cls, v: str, values, **kwargs):
        if v != values["username_from_db"]:
            raise ValueError("Username does not exist")
        return v


@router.post("/set_password")
async def set_new_password_after_reset(
    userdata: UpdataUserData,
    email: EmailStr = Depends(get_email_from_restore_token)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    userdata_from_db = await get_userdata_from_email(email)
    if userdata_from_db is None:
        raise credentials_exception

    try:
        DataFromUser(username=userdata.username,
                     username_from_db=userdata_from_db.username)
    except ValidationError as err:
        raise HTTPException(status_code=422,
                            detail=jsonable_encoder(err.errors()))

    await replace_password(userdata.username,
                           get_password_hash(userdata.password))

    delete_all_refresh_tokens(userdata.username)

    return {"operation": "set_password", "successful": True}
