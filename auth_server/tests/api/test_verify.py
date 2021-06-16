from fastapi.testclient import TestClient
from auth_server.main import app
import pytest
from auth_server.services.password import get_password_hash
import json


@pytest.fixture
def save_userdata_to_redis(redisdb):
    def _save_userdata_to_redis(userdata):
        data = {
            "fullname": userdata["fullname"],
            "email": userdata["email"],
            "hash_password": get_password_hash(userdata["password"])
        }
        namespase = "userdata:"
        redisdb.set(namespase + userdata["username"], json.dumps(data))
    return _save_userdata_to_redis


def test_correct_token(migrated_postgres_connection, redisdb, url, maildev,
                       create_jwt_token, save_userdata_to_redis):
    with TestClient(app, base_url=url) as client:
        userdata = {
            "username": "qwerty",
            "fullname": "qwe qwe",
            "email": "qwe@qwe.com",
            "password": "supersecret"
        }
        save_userdata_to_redis(userdata)

        token = create_jwt_token({"sub": "qwerty", "scope": "registration"})

        payload = {
            "token": token
        }
        response = client.post("/verify", json=payload)
        assert response.status_code == 200
        assert response.json() == {"username": "qwerty"}


def test_incorrect_username(migrated_postgres_connection, redisdb, url,
                            create_jwt_token, save_userdata_to_redis):
    with TestClient(app, base_url=url) as client:
        userdata = {
            "username": "qwerty",
            "fullname": "qwe qwe",
            "email": "qwe@qwe.com",
            "password": "supersecret"
        }
        save_userdata_to_redis(userdata)

        token = create_jwt_token({"sub": "qwerty1", "scope": "registration"})

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


def test_expired_token(migrated_postgres_connection, redisdb, url,
                       create_jwt_token, save_userdata_to_redis):
    with TestClient(app, base_url=url) as client:
        userdata = {
            "username": "qwerty",
            "fullname": "qwe qwe",
            "email": "qwe@qwe.com",
            "password": "supersecret"
        }
        save_userdata_to_redis(userdata)

        token = create_jwt_token({"sub": "qwerty", "scope": "registration"},
                                 is_expire=True)

        payload = {
            "token": token
        }
        response = client.post("/verify", json=payload)
        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}


def test_correct_token_no_data_in_db(migrated_postgres_connection,
                                     redisdb, url, create_jwt_token,
                                     save_userdata_to_redis):
    with TestClient(app, base_url=url) as client:
        token = create_jwt_token({"sub": "qwerty", "scope": "registration"})

        payload = {
            "token": token
        }
        response = client.post("/verify", json=payload)
        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}


def test_repeated_request(migrated_postgres_connection, redisdb, url, maildev,
                          create_jwt_token, save_userdata_to_redis):
    with TestClient(app, base_url=url) as client:
        userdata = {
            "username": "qwerty",
            "fullname": "qwe qwe",
            "email": "qwe@qwe.com",
            "password": "supersecret"
        }
        save_userdata_to_redis(userdata)

        token = create_jwt_token({"sub": "qwerty", "scope": "registration"})

        payload = {
            "token": token
        }
        response = client.post("/verify", json=payload)
        assert response.status_code == 200
        assert response.json() == {"username": "qwerty"}

        response = client.post("/verify", json=payload)
        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}


def test_incorrect_scope(migrated_postgres_connection, redisdb, url, maildev,
                         create_jwt_token, save_userdata_to_redis):
    with TestClient(app, base_url=url) as client:
        userdata = {
            "username": "qwerty",
            "fullname": "qwe qwe",
            "email": "qwe@qwe.com",
            "password": "supersecret"
        }
        save_userdata_to_redis(userdata)

        token = create_jwt_token({"sub": "qwerty", "scope": "user"})

        payload = {
            "token": token
        }
        response = client.post("/verify", json=payload)
        assert response.status_code == 401
        assert response.json() == {"detail": "Could not validate credentials"}
