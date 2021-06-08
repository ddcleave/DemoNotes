# проверяем акцес токен
# создаем токен, отправляем его на мыло
from datetime import timedelta

from auth_server.api.dependencies.get_user import get_user
from auth_server.core.config import Settings, get_settings
from auth_server.db.database import database
from auth_server.db.queries import get_user_from_db
from auth_server.email_templates.template import simple_template_for_email
from auth_server.models import ResponseAuth
from auth_server.services.jwt import create_jwt_token
from auth_server.services.mail_server import mail_server
from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi_mail import MessageSchema

router = APIRouter()

# 
@router.post("/reset_password", response_model=ResponseAuth)
async def reset_password(
    background_tasks: BackgroundTasks,
    user: str = Depends(get_user),
    settings: Settings = Depends(get_settings)
):
    res = await database.fetch_one(get_user_from_db(user))
    if not res:
        # вызвать ошибку
        pass
    email = res["email"]
    # сделать темплейт для сброса пароля
    token_expires = timedelta(minutes=settings.email_token_expire_minutes)
    token = create_jwt_token(
        data={"sub": user, "scope": "restore"},
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        expires_delta=token_expires
    )
    message = MessageSchema(
        subject="Reset password",
        recipients=[email],
        body=simple_template_for_email(token),
        subtype="html"
    )
    background_tasks.add_task(mail_server.send_message, message)
    return {"operation": "reset_password", "successful": True}
