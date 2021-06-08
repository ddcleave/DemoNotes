from fastapi_mail import FastMail
from auth_server.core.config import mail_conf


mail_server = FastMail(mail_conf)
