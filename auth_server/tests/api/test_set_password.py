# задать рефреш токены
# нужно сгенерировать рестор токен
# подставить пароль
# сделать пост запрос к сет_пассворд
# проверить что успешно
# проверить, что сброшены все рефреш токены
# проверить, что пароль был изменен
from auth_server.services.password import get_password_hash, verify_password
from auth_server.db.queries import get_user_from_db, insert_new_user
from auth_server.services.jwt import create_jwt_token
from auth_server.core.config import get_settings
from fastapi.testclient import TestClient
from auth_server.main import app
from uuid import uuid4
import json
from datetime import timedelta


def test_token_exists(migrated_postgres_connection, redisdb, url):
    username = "qwerty"
    password = "supersecret"
    new_password = "supersecret2"
    refresh_token = uuid4()
    fingerprint = "4650b687b0c11f970b642f18316ccfe8"
    migrated_postgres_connection.execute(insert_new_user(
        username,
        "qwe qwe",
        "qwe@qwe.com",
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
            "sub": username,
            "scope": "restore"
        },
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        expires_delta=timedelta(
            minutes=settings.access_token_expire_minutes)
    )
    redisdb.set(namespase + str_r_token, json.dumps(r_token_dict))
    with TestClient(app, base_url=url) as client:
        payload = {"token": restore_token, "password": new_password}
        response = client.post("/set_password", data=payload)
        assert response.status_code == 200
        assert response.json() == {"operation": "set_password", "successful": True}
    assert redisdb.exists(namespase_all_r_tokens_of_user + username) == False
    assert redisdb.exists(namespase + str_r_token) == False
    user_db = migrated_postgres_connection.execute(get_user_from_db(username))
    for row in user_db:
        assert verify_password(new_password, row["hashed_password"])
