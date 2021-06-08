from auth_server.services.password import get_password_hash
from auth_server.db.queries import insert_new_user
from fastapi.testclient import TestClient
from auth_server.main import app
from uuid import uuid4
import json
from datetime import timedelta
from auth_server.core.config import get_settings
from auth_server.services.jwt import create_jwt_token
from bs4 import BeautifulSoup
from jose import JWTError, jwt
from requests import Session


def test_token_exists(migrated_postgres_connection, redisdb, url, maildev):
    username = "qwerty"
    migrated_postgres_connection.execute(insert_new_user(
        username, "qwe", "qwe@qwe.com", get_password_hash("supersecret")))
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
        response = client.post("/reset_password", cookies=cookies)
        assert response.status_code == 200
        assert response.json() == {
            "operation": "reset_password",
            "successful": True
        }
    assert redisdb.exists(namespase_all_r_tokens_of_user + username) == True
    assert redisdb.exists(namespase + str_r_token) == True
    with Session() as em:
        res = em.get("http://" + get_settings().test_mail_server +
                     ":1080/email")
        result = res.json()
        soup = BeautifulSoup(result[0]['html'], features="lxml")
        token = soup.html.body.p.br.next_sibling
        settings = get_settings()
        try:
            payload_token = jwt.decode(token, settings.secret_key,
                                       algorithms=[settings.algorithm])
            username_from_email: str = payload_token.get("sub")
        except JWTError:
            assert False
        assert username == username_from_email
