from auth_server.services.password import get_password_hash, verify_password
from auth_server.db.queries import get_user_from_db, insert_new_user
from auth_server.services.jwt import create_jwt_token
from auth_server.core.config import get_settings
from fastapi.testclient import TestClient
from auth_server.main import app
from uuid import uuid4
import json
from datetime import timedelta


def test_set_password(migrated_postgres_connection, redisdb, url):
    username = "qwerty"
    password = "supersecret"
    new_password = "supersecret2"
    email = "qwe@qwe.com"
    refresh_token = uuid4()
    fingerprint = "4650b687b0c11f970b642f18316ccfe8"

    migrated_postgres_connection.execute(insert_new_user(
        username,
        "qwe qwe",
        email,
        get_password_hash(password)
    ))

    r_token_dict = {
        "username": username,
        "fingerprint": fingerprint,
        "ip": "testclient"
    }
    str_r_token = str(refresh_token)

    namespase = "r_token:"
    namespase_all_r_tokens_of_user = "rt_user"
    redisdb.hset(
        namespase_all_r_tokens_of_user + username,
        fingerprint,
        str_r_token
    )

    settings = get_settings()

    restore_token = create_jwt_token(
        data={
            "sub": email,
            "scope": "restore"
        },
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        expires_delta=timedelta(
            minutes=settings.access_token_expire_minutes)
    )
    redisdb.set(namespase + str_r_token, json.dumps(r_token_dict))

    with TestClient(app, base_url=url) as client:
        payload = {
            "userdata": {
                "username": username,
                "password": new_password
            },
            "token": restore_token
        }
        response = client.post("/set_password", json=payload)
        assert response.status_code == 200
        assert response.json() == {
            "operation": "set_password",
            "successful": True
        }
    assert redisdb.exists(namespase_all_r_tokens_of_user + username) == False
    assert redisdb.exists(namespase + str_r_token) == False

    user_db = migrated_postgres_connection.execute(get_user_from_db(username))
    for row in user_db:
        assert verify_password(new_password, row["hashed_password"])


def test_set_password_different_username(
    migrated_postgres_connection, redisdb, url
):
    username = "qwerty"
    password = "supersecret"
    new_password = "supersecret2"
    email = "qwe@qwe.com"
    refresh_token = uuid4()
    fingerprint = "4650b687b0c11f970b642f18316ccfe8"
    wrong_username = "qwerty2"

    migrated_postgres_connection.execute(insert_new_user(
        username,
        "qwe qwe",
        email,
        get_password_hash(password)
    ))

    r_token_dict = {
        "username": username,
        "fingerprint": fingerprint,
        "ip": "testclient"
    }
    str_r_token = str(refresh_token)

    namespase = "r_token:"
    namespase_all_r_tokens_of_user = "rt_user"
    redisdb.hset(
        namespase_all_r_tokens_of_user + username,
        fingerprint,
        str_r_token
    )

    settings = get_settings()

    restore_token = create_jwt_token(
        data={
            "sub": email,
            "scope": "restore"
        },
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        expires_delta=timedelta(
            minutes=settings.access_token_expire_minutes)
    )
    redisdb.set(namespase + str_r_token, json.dumps(r_token_dict))

    with TestClient(app, base_url=url) as client:
        payload = {
            "userdata": {
                "username": wrong_username,
                "password": new_password
            },
            "token": restore_token
        }
        response = client.post("/set_password", json=payload)
        assert response.status_code == 422

    assert redisdb.exists(namespase_all_r_tokens_of_user + username) == True
    assert redisdb.exists(namespase + str_r_token) == True

    user_db = migrated_postgres_connection.execute(get_user_from_db(username))
    for row in user_db:
        assert verify_password(password, row["hashed_password"])
