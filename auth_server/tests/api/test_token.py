import pytest
from auth_server.main import app
from fastapi.testclient import TestClient


def test_user_exists_in_db(url, create_account):
    userdata = {
        "username": "qwerty",
        "full_name": "qwe",
        "email": "qwe@qwe.com",
        "password": "supersecret"
    }
    create_account(userdata)

    with TestClient(app, base_url=url) as client:
        payload = {
            "username": "qwerty",
            "password": "supersecret",
            "fingerprint": "4650b687b0c11f970b642f18316ccfe8"
        }
        response = client.post("/token", data=payload)
    assert response.status_code == 200
    assert response.json() == {"operation": "login",
                               "successful": True}


def test_user_not_exists_in_db(migrated_postgres_connection, url):
    with TestClient(app, base_url=url) as client:
        payload = {
            "username": "qwerty",
            "password": "supersecret",
            "fingerprint": "4650b687b0c11f970b642f18316ccfe8"
        }
        response = client.post("/token", data=payload)
        assert response.status_code == 401
        assert response.json() == {"detail": "Incorrect username or password"}


test_cases = {
    "correct_data": (
        {
            "username": "qwerty",
            "password": "supersecret",
            "fingerprint": "4650b687b0c11f970b642f18316ccfe8"
        },
        {
            "status": 200,
            "json": {
                "operation": "login",
                "successful": True
            }
        }
    ),
    "short_password": (
        {
            "username": "qwerty",
            "password": "secret",
            "fingerprint": "4650b687b0c11f970b642f18316ccfe8"
        },
        {
            "status": 422,
            "json": {
                'detail': [
                    {
                        'ctx': {'limit_value': 8},
                        'loc': ['body', 'password'],
                        'msg': 'ensure this value has at least 8 characters',
                        'type': 'value_error.any_str.min_length'
                    }
                ]
            }
        }
    ),
    "too_long_password": (
        {
            "username": "qwerty",
            "password": 'a' * 51,
            "fingerprint": "4650b687b0c11f970b642f18316ccfe8"
        },
        {
            "status": 422,
            "json": {
                'detail': [
                    {
                        'ctx': {'limit_value': 50},
                        'loc': ['body', 'password'],
                        'msg': 'ensure this value has at most 50 characters',
                        'type': 'value_error.any_str.max_length'
                    }
                ]
            }
        }
    ),
    "short_username": (
        {
            "username": "qw",
            "password": "supersecret",
            "fingerprint": "4650b687b0c11f970b642f18316ccfe8"
        },
        {
            "status": 422,
            "json": {
                'detail': [
                    {
                        'ctx': {'limit_value': 3},
                        'loc': ['body', 'username'],
                        'msg': 'ensure this value has at least 3 characters',
                        'type': 'value_error.any_str.min_length'
                    }
                ]
            }
        }
    ),
    "too_long_username": (
        {
            "username": "a" * 51,
            "password": "supersecret",
            "fingerprint": "4650b687b0c11f970b642f18316ccfe8"
        },
        {
            "status": 422,
            "json": {
                'detail': [
                    {
                        'ctx': {'limit_value': 50},
                        'loc': ['body', 'username'],
                        'msg': 'ensure this value has at most 50 characters',
                        'type': 'value_error.any_str.max_length'
                    }
                ]
            }
        }
    ),
    "short_fingerprint": (
        {
            "username": "qwerty",
            "password": "supersecret",
            "fingerprint": "4650"
        },
        {
            "status": 422,
            "json": {
                'detail': [
                    {
                        'ctx': {'limit_value': 32},
                        'loc': ['body', 'fingerprint'],
                        'msg': 'ensure this value has at least 32 characters',
                        'type': 'value_error.any_str.min_length'
                    }
                ]
            }
        }
    ),
    "too_long_fingerprint": (
        {
            "username": "qwerty",
            "password": "supersecret",
            "fingerprint": "4" * 257
        },
        {
            "status": 422,
            "json": {
                'detail': [
                    {
                        'ctx': {'limit_value': 256},
                        'loc': ['body', 'fingerprint'],
                        'msg': 'ensure this value has at most 256 characters',
                        'type': 'value_error.any_str.max_length'
                    }
                ]
            }
        }
    ),
    "without_fingerprint": (
        {
            "username": "qwerty",
            "password": "supersecret",
            "fingerprint": ""
        },
        {
            "status": 422,
            "json": {
                'detail': [
                    {
                        'loc': ['body', 'fingerprint'],
                        'msg': 'field required',
                        'type': 'value_error.missing'
                    }
                ]
            }
        }
    ),
    "without_password": (
        {
            "username": "qwerty",
            "password": "",
            "fingerprint": "4650b687b0c11f970b642f18316ccfe8"
        },
        {
            "status": 422,
            "json": {
                'detail': [
                    {
                        'loc': ['body', 'password'],
                        'msg': 'field required',
                        'type': 'value_error.missing'
                    }
                ]
            }
        }
    ),
    "without_username": (
        {
            "username": "",
            "password": "supersecret",
            "fingerprint": "4650b687b0c11f970b642f18316ccfe8"
        },
        {
            "status": 422,
            "json": {
                'detail': [
                    {
                        'loc': ['body', 'username'],
                        'msg': 'field required',
                        'type': 'value_error.missing'
                    }
                ]
            }
        }
    )
}


@pytest.mark.parametrize("user_data,resp", test_cases.values(),
                         ids=list(test_cases.keys()))
def test_validation(url, user_data, resp, create_account):
    userdata = {
        "username": "qwerty",
        "full_name": "qwe",
        "email": "qwe@qwe.com",
        "password": "supersecret"
    }
    create_account(userdata)

    with TestClient(app, base_url=url) as client:
        response = client.post("/token", data=user_data)
    assert response.status_code == resp["status"]
    assert response.json() == resp["json"]
