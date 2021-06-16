from auth_server.db.schema import users_table
from auth_server.main import app
from auth_server.services.password import verify_password
from fastapi.testclient import TestClient


def test_set_password(migrated_postgres_connection, redisdb, url,
                      create_account, create_refresh_token, create_jwt_token):
    username = "qwerty"
    password = "supersecret"
    new_password = "supersecret2"
    email = "qwe@qwe.com"
    fingerprint = "4650b687b0c11f970b642f18316ccfe8"
    namespase = "r_token:"
    namespase_all_r_tokens_of_user = "rt_user:"

    userdata = {
        "username": username,
        "full_name": "qwe",
        "email": email,
        "password": password
    }
    create_account(userdata)

    token = create_refresh_token(username, fingerprint)

    restore_token = create_jwt_token(data={"sub": email, "scope": "restore"})

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
    assert redisdb.exists(namespase + token) == False

    query = users_table.select().where(
        users_table.c.email == email
    )
    user_db = migrated_postgres_connection.execute(query)

    for row in user_db:
        assert verify_password(new_password, row["hashed_password"])


def test_set_password_different_username(
    migrated_postgres_connection, redisdb, url,
    create_account, create_refresh_token, create_jwt_token
):
    username = "qwerty"
    password = "supersecret"
    new_password = "supersecret2"
    email = "qwe@qwe.com"
    fingerprint = "4650b687b0c11f970b642f18316ccfe8"
    wrong_username = "qwerty2"
    namespase = "r_token:"
    namespase_all_r_tokens_of_user = "rt_user:"

    userdata = {
        "username": username,
        "full_name": "qwe",
        "email": email,
        "password": password
    }
    create_account(userdata)

    token = create_refresh_token(username, fingerprint)

    restore_token = create_jwt_token(data={"sub": email, "scope": "restore"})

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
    assert redisdb.exists(namespase + token) == True
    query = users_table.select().where(
        users_table.c.email == email
    )
    user_db = migrated_postgres_connection.execute(query)

    for row in user_db:
        assert verify_password(password, row["hashed_password"])
