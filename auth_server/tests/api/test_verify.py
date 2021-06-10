from auth_server.core.config import get_settings
from fastapi.testclient import TestClient
from auth_server.main import app
import pytest
from auth_server.services.jwt import create_jwt_token
from datetime import timedelta
from auth_server.services.password import get_password_hash
import json


def test_correct_token(migrated_postgres_connection, redisdb, url, maildev):
    with TestClient(app, base_url=url) as client:
        settings = get_settings()
        token_expires = timedelta(minutes=settings.email_token_expire_minutes)
        data = {
            "fullname": "qwe qwe",
            "email": "qwe@qwe.com",
            "hash_password": get_password_hash("supersecret")
        }
        exp = settings.email_token_expire_minutes * 60
        namespase = "userdata:"
        with redisdb.pipeline() as pipe:
            pipe.multi()
            pipe.set(namespase + "qwerty", json.dumps(data))
            pipe.expire(namespase + "qwerty", exp)
            pipe.execute()

        token = create_jwt_token(
            data={"sub": "qwerty", "scope": "registration"},
            secret_key=settings.secret_key,
            algorithm=settings.algorithm,
            expires_delta=token_expires
        )
        payload = {
            "token": token
        }
        response = client.post("/verify", json=payload)
        assert response.status_code == 200
        assert response.json() == {"username": "qwerty"}


# что надо проверить
# некоректные данные в токене
# корректный токен, но в базе нет данных
# истекший токен


def test_incorrect_username(migrated_postgres_connection, redisdb, url):
    with TestClient(app, base_url=url) as client:
        settings = get_settings()
        token_expires = timedelta(minutes=settings.email_token_expire_minutes)
        data = {
            "fullname": "qwe qwe",
            "email": "qwe@qwe.com",
            "hash_password": get_password_hash("supersecret")
        }
        exp = settings.email_token_expire_minutes * 60
        namespase = "userdata:"
        with redisdb.pipeline() as pipe:
            pipe.multi()
            pipe.set(namespase + "qwerty", json.dumps(data))
            pipe.expire(namespase + "qwerty", exp)
            pipe.execute()

        token = create_jwt_token(
            data={"sub": "qwerty1", "scope": "registration"},
            secret_key=settings.secret_key,
            algorithm=settings.algorithm,
            expires_delta=token_expires
        )
        payload = {
            "token": token
        }
        response = client.post("/verify", json=payload)
        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}


def test_incorrect_token(migrated_postgres_connection, redisdb, url):
    with TestClient(app, base_url=url) as client:
        token = "a" * 100
        payload = {
            "token": token
        }
        response = client.post("/verify", json=payload)
        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}


def test_expired_token(migrated_postgres_connection, redisdb, url):
    with TestClient(app, base_url=url) as client:
        settings = get_settings()
        token_expires = timedelta(minutes=settings.email_token_expire_minutes)
        data = {
            "fullname": "qwe qwe",
            "email": "qwe@qwe.com",
            "hash_password": get_password_hash("supersecret")
        }
        exp = 0
        namespase = "userdata:"
        with redisdb.pipeline() as pipe:
            pipe.multi()
            pipe.set(namespase + "qwerty", json.dumps(data))
            pipe.expire(namespase + "qwerty", exp)
            pipe.execute()

        token = create_jwt_token(
            data={"sub": "qwerty", "scope": "registration"},
            secret_key=settings.secret_key,
            algorithm=settings.algorithm,
            expires_delta=token_expires
        )
        payload = {
            "token": token
        }
        response = client.post("/verify", json=payload)
        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}


def test_correct_token_no_data_in_db(migrated_postgres_connection,
                                     redisdb, url):
    with TestClient(app, base_url=url) as client:
        settings = get_settings()
        token_expires = timedelta(minutes=settings.email_token_expire_minutes)

        token = create_jwt_token(
            data={"sub": "qwerty", "scope": "registration"},
            secret_key=settings.secret_key,
            algorithm=settings.algorithm,
            expires_delta=token_expires
        )
        payload = {
            "token": token
        }
        response = client.post("/verify", json=payload)
        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}


def test_repeated_request(migrated_postgres_connection, redisdb, url, maildev):
    with TestClient(app, base_url=url) as client:
        settings = get_settings()
        token_expires = timedelta(minutes=settings.email_token_expire_minutes)
        data = {
            "fullname": "qwe qwe",
            "email": "qwe@qwe.com",
            "hash_password": get_password_hash("supersecret")
        }
        exp = settings.email_token_expire_minutes * 60
        namespase = "userdata:"
        with redisdb.pipeline() as pipe:
            pipe.multi()
            pipe.set(namespase + "qwerty", json.dumps(data))
            pipe.expire(namespase + "qwerty", exp)
            pipe.execute()

        token = create_jwt_token(
            data={"sub": "qwerty", "scope": "registration"},
            secret_key=settings.secret_key,
            algorithm=settings.algorithm,
            expires_delta=token_expires
        )
        payload = {
            "token": token
        }
        response = client.post("/verify", json=payload)
        assert response.status_code == 200
        assert response.json() == {"username": "qwerty"}

        response = client.post("/verify", json=payload)
        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}


def test_incorrect_scope(migrated_postgres_connection, redisdb, url, maildev):
    with TestClient(app, base_url=url) as client:
        settings = get_settings()
        token_expires = timedelta(minutes=settings.email_token_expire_minutes)
        data = {
            "fullname": "qwe qwe",
            "email": "qwe@qwe.com",
            "hash_password": get_password_hash("supersecret")
        }
        exp = settings.email_token_expire_minutes * 60
        namespase = "userdata:"
        with redisdb.pipeline() as pipe:
            pipe.multi()
            pipe.set(namespase + "qwerty", json.dumps(data))
            pipe.expire(namespase + "qwerty", exp)
            pipe.execute()

        token = create_jwt_token(
            data={"sub": "qwerty", "scope": "user"},
            secret_key=settings.secret_key,
            algorithm=settings.algorithm,
            expires_delta=token_expires
        )
        payload = {
            "token": token
        }
        response = client.post("/verify", json=payload)
        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}