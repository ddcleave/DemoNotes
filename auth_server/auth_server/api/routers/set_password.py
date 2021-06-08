# вытаскиваем токен из ссылки, проверяем его валидность
# получаем новый пароль
# сбрасываем все рефреш токены
# устанавливаем новый пароль
from auth_server.api.dependencies.get_userdata_from_token import \
    get_username_from_restore_token
from auth_server.services.password import get_password_hash
from auth_server.api.dependencies.tokens import delete_all_refresh_tokens
from auth_server.api.dependencies.queries_to_db import replace_password
from fastapi import APIRouter, Depends, Form


router = APIRouter()


@router.post("/set_password")
async def set_new_password_after_reset(
    # token: str,
    username: str = Depends(get_username_from_restore_token),
    password: str = Form(..., min_length=8, max_length=50)
):
    # сбросить рефреши по юзернейму
    delete_all_refresh_tokens(username)
    # изменить пароль по юзернейму в базе
    await replace_password(username, get_password_hash(password))
    return {"operation": "set_password", "successful": True}
