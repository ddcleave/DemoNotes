from auth_server.services.password import get_password_hash
from auth_server.db.queries import insert_new_user
from fastapi.testclient import TestClient
from auth_server.main import app
from auth_server.core.config import get_settings
from bs4 import BeautifulSoup
from jose import JWTError, jwt
from requests import Session


def test_token_exists(migrated_postgres_connection, url, maildev):
    username = "qwerty"
    email = "qwe@qwe.com"
    migrated_postgres_connection.execute(insert_new_user(
        username, "qwe", email, get_password_hash("supersecret")))
    settings = get_settings()

    with TestClient(app, base_url=url) as client:
        response = client.post("/reset_password", json={"email": email})
        assert response.status_code == 200
        assert response.json() == {
            "operation": "reset_password",
            "successful": True
        }
    with Session() as em:
        res = em.get("http://" + get_settings().test_mail_server +
                     ":1080/email")
        result = res.json()
        soup = BeautifulSoup(result[0]['html'], features="lxml")
        token = soup.html.body.find('a').text.split('token=', 1)[1]
        settings = get_settings()
        try:
            payload_token = jwt.decode(token, settings.secret_key,
                                       algorithms=[settings.algorithm])
            email_from_token = payload_token.get("sub")
        except JWTError:
            assert False
        assert email == email_from_token
