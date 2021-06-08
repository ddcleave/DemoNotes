from auth_server.services.alembic import make_alembic_config
import functools
from sqlalchemy_utils import create_database, drop_database
import pytest
import asyncio
from auth_server.db.queries import insert_new_user

from auth_server.services.password import get_password_hash
from bs4 import BeautifulSoup
from fastapi.testclient import TestClient
from requests import Session
import databases
import uuid
from yarl import URL
from alembic.command import upgrade
import os
import importlib
from auth_server.main import app
from auth_server.core.config import get_settings

# database = databases.Database(get_settings().database_url)


# @app.on_event("startup")
# async def startup():
#     await database.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


# @pytest.mark.asyncio
# async def test_token():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         payload = {
#             "username": "johndoe",
#             "password": "secret"
#         }
#         response = await ac.post("/token", data=payload)
#     assert response.status_code == 200


# def async_adapter(wrapped_func):
#     """
#     Decorator used to run async test cases.
#     """

#     @functools.wraps(wrapped_func)
#     def run_sync(*args, **kwargs):
#         loop = asyncio.new_event_loop()
#         task = wrapped_func(*args, **kwargs)
#         return loop.run_until_complete(task)

#     return run_sync


@pytest.fixture
def postgres():
    postgres_url = get_settings().test_database_url
    create_database(postgres_url)

    try:
        yield postgres_url
    finally:
        drop_database(postgres_url)


@pytest.fixture
def alembic_config(postgres):
    return make_alembic_config(config_file="alembic-dev.ini",
                               ini_section="alembic",
                               pg_url=postgres)


@pytest.fixture
async def migrated_postgres(alembic_config, postgres):
    upgrade(alembic_config, 'head')
    return postgres


@pytest.fixture
async def prepare(migrated_postgres):
    async with databases.Database(migrated_postgres) as database:
        await database.execute(insert_new_user(
            "qwerty", "qwe", "qwe@qwe.com", get_password_hash("supersecret")
            ))


def test_token(prepare):
    # from auth_server.main import app

    with TestClient(app, base_url="http://localtest.me") as client:
        payload = {
            "username": "qwerty",
            "password": "supersecret",
            "fingerprint": "4650b687b0c11f970b642f18316ccfe8"
        }
        response = client.post("/token", data=payload)
        assert response.status_code == 200
        assert response.json() == {"operation": "login",
                                   "successful": True}


@pytest.fixture
async def prepare2(migrated_postgres):

    async with databases.Database(migrated_postgres) as database:
        await database.execute(insert_new_user(
            "qwerty", "qwe", "qwe@qwe.com", get_password_hash("supersecret")
            ))


def test_token2(prepare2):
    # from auth_server.main import app

    with TestClient(app, base_url="http://localtest.me") as client:
        payload = {
            "username": "qwerty2",
            "password": "supersecret",
            "fingerprint": "4650b687b0c11f970b642f18316ccfe8"
        }
        response = client.post("/token", data=payload)
        assert response.status_code != 200
        assert response.json() != {"operation": "login",
                                   "successful": True}





# def test_signup():
#     with TestClient(app, base_url="http://localtest.me") as client:
#         payload = {
#             "username": "johndoe4678",
#             "password": "secret23456",
#             "email": "jjjjjj4678@jru.com",
#             "full_name": "ddfsfsdfssf"
#         }
#         response = client.post("/signup", data=payload)
#         assert response.status_code == 200
#         assert response.json() == {"operation": "signup", "successful": True}


# def test_email_token():
#     with Session() as em:
#         res = em.get("http://maildev:1080/email")
#         result = res.json()
#         soup = BeautifulSoup(result[0]['html'], features="lxml")
#         token = soup.html.body.p.br.next_sibling
#         with TestClient(app, base_url="http://localtest.me") as client:
#             url = "/verify?token=" + token
#             response = client.get(url)
#             assert response.status_code == 200
#             assert response.json() == {"username": "johndoe4678"}


# def test_refresh():
#     with TestClient(app, base_url="http://localtest.me") as client:
#         payload = {
#             "username": "johndoe4678",
#             "password": "secret23456",
#             "fingerprint": "123456"
#         }
#         response = client.post("/token", data=payload)
#         payload = {"fingerprint": "123456"}
#         response = client.post("/refresh", data=payload)
#         assert response.status_code == 200
#         assert response.json() == {"operation": "refresh", "successful": True}
