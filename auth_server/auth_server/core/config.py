from functools import lru_cache
from pydantic import BaseSettings, PostgresDsn, RedisDsn
from fastapi_mail import ConnectionConfig


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    email_token_expire_minutes: int
    refresh_token_expire_days: int
    database_url: PostgresDsn
    domain: str
    redis_url: RedisDsn
    testing: bool
    test_database_url: PostgresDsn
    test_redis_url: RedisDsn
    mail_username: str = ""
    mail_password: str = ""
    mail_from: str
    mail_port: int
    mail_server: str
    test_mail_server: str
    mail_tls: bool
    mail_ssl: bool
    test_mail_username: str = ""
    test_mail_password: str = ""
    test_mail_from: str
    test_mail_port: int
    test_mail_server: str
    test_mail_server: str
    test_mail_tls: bool
    test_mail_ssl: bool
    https: bool

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()


if get_settings().testing:
    mail_conf = ConnectionConfig(
        MAIL_USERNAME=get_settings().test_mail_username,
        MAIL_PASSWORD=get_settings().test_mail_password,
        MAIL_FROM=get_settings().test_mail_from,
        MAIL_PORT=get_settings().test_mail_port,
        MAIL_SERVER=get_settings().test_mail_server,
        MAIL_TLS=get_settings().test_mail_tls,
        MAIL_SSL=get_settings().test_mail_ssl,
        TEMPLATE_FOLDER='./auth_server/email_templates'
    )
else:
    mail_conf = ConnectionConfig(
        MAIL_USERNAME=get_settings().mail_username,
        MAIL_PASSWORD=get_settings().mail_password,
        MAIL_FROM=get_settings().mail_from,
        MAIL_PORT=get_settings().mail_port,
        MAIL_SERVER=get_settings().mail_server,
        MAIL_TLS=get_settings().mail_tls,
        MAIL_SSL=get_settings().mail_ssl,
        TEMPLATE_FOLDER='./auth_server/email_templates'
    )
