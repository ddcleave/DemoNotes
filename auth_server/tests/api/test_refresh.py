from fastapi.testclient import TestClient
from auth_server.main import app
from uuid import uuid4
import json


def test_token_exists(migrated_postgres, redisdb, url):
    refresh_token = uuid4()
    fingerprint = "4650b687b0c11f970b642f18316ccfe8"
    r_token_dict = {
        "username": "qwerty",
        "fingerprint": fingerprint,
        "ip": "testclient"
    }
    str_r_token = str(refresh_token)
    namespase = "r_token:"
    redisdb.set(namespase + str_r_token, json.dumps(r_token_dict))
    with TestClient(app, base_url=url) as client:
        payload = {"fingerprint": fingerprint}
        cookies = {"refresh_token": str_r_token}
        response = client.post("/refresh", data=payload, cookies=cookies)
        assert response.status_code == 200
        assert response.json() == {"operation": "refresh", "successful": True}


def test_without_refresh_cookie(migrated_postgres, redisdb, url):
    fingerprint = "4650b687b0c11f970b642f18316ccfe8"
    with TestClient(app, base_url=url) as client:
        payload = {"fingerprint": fingerprint}
        response = client.post("/refresh", data=payload)
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}


def test_fingerprint_not_equil(migrated_postgres, redisdb, url):
    refresh_token = uuid4()
    fingerprint = "4650b687b0c11f970b642f18316ccfe8"
    r_token_dict = {
        "username": "qwerty",
        "fingerprint": fingerprint,
        "ip": "testclient"
    }
    str_r_token = str(refresh_token)
    namespase = "r_token:"
    redisdb.set(namespase + str_r_token, json.dumps(r_token_dict))
    with TestClient(app, base_url=url) as client:
        payload = {"fingerprint": "4650b687b0c11f970b642f18316ccfe9"}
        cookies = {"refresh_token": str_r_token}
        response = client.post("/refresh", data=payload, cookies=cookies)
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}


def test_ip_not_equil(migrated_postgres, redisdb, url):
    refresh_token = uuid4()
    fingerprint = "4650b687b0c11f970b642f18316ccfe8"
    r_token_dict = {
        "username": "qwerty",
        "fingerprint": fingerprint,
        "ip": "test"
    }
    str_r_token = str(refresh_token)
    namespase = "r_token:"
    redisdb.set(namespase + str_r_token, json.dumps(r_token_dict))
    with TestClient(app, base_url=url) as client:
        payload = {"fingerprint": fingerprint}
        cookies = {"refresh_token": str_r_token}
        response = client.post("/refresh", data=payload, cookies=cookies)
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}


def test_reuse_after_success(migrated_postgres, redisdb, url):
    refresh_token = uuid4()
    fingerprint = "4650b687b0c11f970b642f18316ccfe8"
    r_token_dict = {
        "username": "qwerty",
        "fingerprint": fingerprint,
        "ip": "testclient"
    }
    str_r_token = str(refresh_token)
    namespase = "r_token:"
    redisdb.set(namespase + str_r_token, json.dumps(r_token_dict))
    with TestClient(app, base_url=url) as client:
        payload = {"fingerprint": fingerprint}
        cookies = {"refresh_token": str_r_token}
        response = client.post("/refresh", data=payload, cookies=cookies)
        assert response.status_code == 200
        assert response.json() == {"operation": "refresh", "successful": True}
        response = client.post("/refresh", data=payload, cookies=cookies)
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}


def test_reuse_after_use_nonvalid_fingerprint(migrated_postgres, redisdb, url):
    refresh_token = uuid4()
    fingerprint = "4650b687b0c11f970b642f18316ccfe8"
    r_token_dict = {
        "username": "qwerty",
        "fingerprint": fingerprint,
        "ip": "testclient"
    }
    str_r_token = str(refresh_token)
    namespase = "r_token:"
    redisdb.set(namespase + str_r_token, json.dumps(r_token_dict))
    with TestClient(app, base_url=url) as client:
        payload = {"fingerprint": "4650b687b0c11f970b642f18316ccfe9"}
        cookies = {"refresh_token": str_r_token}
        response = client.post("/refresh", data=payload, cookies=cookies)
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}
        payload = {"fingerprint": fingerprint}
        response = client.post("/refresh", data=payload, cookies=cookies)
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}


def test_reuse_after_use_nonvalid_ip(migrated_postgres, redisdb, url):
    refresh_token = uuid4()
    fingerprint = "4650b687b0c11f970b642f18316ccfe8"
    r_token_dict = {
        "username": "qwerty",
        "fingerprint": fingerprint,
        "ip": "nonvalid_ip"
    }
    str_r_token = str(refresh_token)
    namespase = "r_token:"
    redisdb.set(namespase + str_r_token, json.dumps(r_token_dict))
    with TestClient(app, base_url=url) as client:
        payload = {"fingerprint": "4650b687b0c11f970b642f18316ccfe9"}
        cookies = {"refresh_token": str_r_token}
        response = client.post("/refresh", data=payload, cookies=cookies)
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}
        result = redisdb.get(namespase + str_r_token)
        assert result == None # noqa
