from datetime import timedelta

from auth_server.core.config import Settings, get_settings
from auth_server.db.database import database
from auth_server.db.queries import get_user_from_db
from auth_server.models import ResponseAuth
from auth_server.models.models import EmailRequest
from auth_server.services.jwt import create_jwt_token
from auth_server.services.mail_server import mail_server
from auth_server.utils.create_url import create_url_for_email
from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi_mail import MessageSchema

router = APIRouter()


@router.post("/reset_password", response_model=ResponseAuth)
async def reset_password(
    background_tasks: BackgroundTasks,
    item: EmailRequest,
    settings: Settings = Depends(get_settings)
):
    res = await database.fetch_one(get_user_from_db(item.email))
    if res:
        token_expires = timedelta(minutes=settings.email_token_expire_minutes)
        token = create_jwt_token(
            data={"sub": item.email, "scope": "restore"},
            secret_key=settings.secret_key,
            algorithm=settings.algorithm,
            expires_delta=token_expires
        )
        message = MessageSchema(
            subject="Reset password",
            recipients=[item.email],
            body={"reset_url": create_url_for_email(
                settings.https, settings.domain, "/reset", {"token": token})},
            subtype="html"
        )
        background_tasks.add_task(mail_server.send_message, message,
                                  template_name="reset.html")
    return {"operation": "reset_password", "successful": True}
