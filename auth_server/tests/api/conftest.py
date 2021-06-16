import json
from uuid import uuid4

from redis.utils import from_url
from jose import jwt
import pytest
from auth_server.core.config import get_settings
from requests import Session
from datetime import datetime, timedelta

from auth_server.db.schema import users_table

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope="session")
def url():
    return "http://" + get_settings().domain


@pytest.fixture
def maildev():
    with Session() as em:
        em.delete("http://" + get_settings().test_mail_server +
                  ":1080/email/all")
        yield
        em.delete("http://" + get_settings().test_mail_server +
                  ":1080/email/all")


@pytest.fixture
def create_account(migrated_postgres_connection):
    def _create_account(userdata):
        query = users_table.insert().values(
            username=userdata["username"],
            full_name=userdata["full_name"],
            email=userdata["email"],
            hashed_password=pwd_context.hash(userdata["password"])
        )
        migrated_postgres_connection.execute(query)

    return _create_account


@pytest.fixture
def create_refresh_token():
    redisdb = from_url(url=get_settings().test_redis_url)

    def _create_refresh_token(username, fingerprint, ip="testclient"):
        data = {
            "username": username,
            "fingerprint": fingerprint,
            "ip": ip
        }
        namespace_rt = "r_token:"
        namespace_all_rt = "rt_user:"

        token = str(uuid4())

        redisdb.set(namespace_rt + token, json.dumps(data))
        redisdb.hset(namespace_all_rt + username,
                     fingerprint,
                     token)
        return token
    return _create_refresh_token


@pytest.fixture
def create_jwt_token():
    algorithm = get_settings().algorithm
    secret_key = get_settings().secret_key

    def _create_access_token(data, is_expire=False):
        to_encode = data.copy()
        if is_expire:
            expire = datetime.utcfromtimestamp(0)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return _create_access_token
