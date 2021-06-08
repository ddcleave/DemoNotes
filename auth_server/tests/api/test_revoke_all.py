from datetime import timedelta
from auth_server.core.config import get_settings
from auth_server.services.jwt import create_jwt_token


# сгенерировать акцес токен
# потом записать данные о рефреш токене
# далее сбросить их с помощью revoke_all
# проверить что токены сброшены
from fastapi.testclient import TestClient
from auth_server.main import app
from uuid import uuid4
import json


def test_token_exists(migrated_postgres, redisdb, url):
    username = "qwerty"
    settings = get_settings()
    namespase_all_r_tokens_of_user = "rt_user"
    access_token = create_jwt_token(
        data={
            "sub": username,
            "scope": "user"
        },
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        expires_delta=timedelta(
            minutes=settings.access_token_expire_minutes)
    )

    refresh_token = uuid4()
    fingerprint = "4650b687b0c11f970b642f18316ccfe8"
    r_token_dict = {
        "username": username,
        "fingerprint": fingerprint,
        "ip": "testclient"
    }
    str_r_token = str(refresh_token)
    namespase = "r_token:"
    redisdb.hset(
        namespase_all_r_tokens_of_user + username,
        fingerprint,
        str_r_token
    )
    redisdb.set(namespase + str_r_token, json.dumps(r_token_dict))
    with TestClient(app, base_url=url) as client:
        cookies = {"access_token": access_token}
        response = client.post("/revoke_all", cookies=cookies)
        assert response.status_code == 200
        assert response.json() == {"operation": "revoke_all", "successful": True}
    assert redisdb.exists(namespase_all_r_tokens_of_user + username) == False
    # print(str_r_token)
    # print(redisdb.get(namespase + str_r_token))
    assert redisdb.exists(namespase + str_r_token) == False
