from datetime import timedelta

from auth_server.api.dependencies.forms import RegistrationForm
from auth_server.api.dependencies.queries_to_db import (exist_email_in_db,
                                                        exist_username_in_db)
from auth_server.api.dependencies.queries_to_redis import (
    save_user_to_redis, set_username_and_email)
from auth_server.core.config import Settings, get_settings
from auth_server.email_templates.template import simple_template_for_email
from auth_server.models import ResponseAuth
from auth_server.models.models import (EmailAndExist, UniqueUsernameAndEmail,
                                       UsernameAndExist)
from auth_server.services.jwt import create_jwt_token
from auth_server.services.mail_server import mail_server
from auth_server.services.password import get_password_hash
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_mail import MessageSchema
from pydantic.error_wrappers import ValidationError


router = APIRouter()


@router.post("/signup", response_model=ResponseAuth)
async def sign_up_with_email(
    background_tasks: BackgroundTasks,
    form_data: RegistrationForm = Depends(),
    settings: Settings = Depends(get_settings)
):
    # дополнительная проверка юзернейма и эмейла на то, что они не используются
    # сначала получаем из постгреса наличие юзернейма и емайла в нем
    exist_username = await exist_username_in_db(form_data.username)
    exist_email = await exist_email_in_db(form_data.email)
    # теперь проверяем их
    try:
        UniqueUsernameAndEmail(
            username=UsernameAndExist(username=form_data.username,
                                      exist_username=exist_username),
            email=EmailAndExist(email=form_data.email,
                                exist_email=exist_email))
    except ValidationError as err:
        raise HTTPException(status_code=422,
                            detail=jsonable_encoder(err.errors()))

    set_username_and_email(
        form_data.username,
        form_data.email,
        settings.email_token_expire_minutes * 60
    )

    save_user_to_redis(
        form_data.username,
        form_data.full_name,
        form_data.email,
        get_password_hash(form_data.password),
        settings.email_token_expire_minutes * 60
    )

    # проверяем на беке уже на то, чтобы он не истек
    token_expires = timedelta(minutes=settings.email_token_expire_minutes)
    token = create_jwt_token(
        data={"sub": form_data.username, "scope": "registration"},
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        expires_delta=token_expires
    )
    if settings.https == True:
        protocol = "https://"
    else:
        protocol = "http://"

    message = MessageSchema(
        subject="Verification",
        recipients=[form_data.email],
        # body=simple_template_for_email(token),
        body={"confirm_url": protocol + settings.domain + "/verify?token=" + token},
        subtype="html"
    )
    background_tasks.add_task(mail_server.send_message, message,
                              template_name="verify.html")

    return {"operation": "signup", "successful": True}
