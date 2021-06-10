from auth_server.core.config import get_settings
import json
import pytest

from auth_server.main import app
from auth_server.services.password import verify_password
from fastapi.testclient import TestClient
from requests import Session
from bs4 import BeautifulSoup
from auth_server.db.queries import insert_new_user
from jose import JWTError, jwt
from auth_server.services.password import get_password_hash


def test_signup(migrated_postgres_connection, redisdb, url, maildev):
    with TestClient(app, base_url=url) as client:
        username = "qwerty"
        payload = {
            "username": username,
            "password": "supersecret",
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe"
        }
        response = client.post("/signup", data=payload)
        assert response.status_code == 200
        assert response.json() == {"operation": "signup", "successful": True}

        namespase = "userdata:"
        res = redisdb.get(namespase + username)
        assert res != None # noqa
        tmp = json.loads(res)
        assert verify_password("supersecret", tmp["hash_password"]) == True # noqa
        assert tmp["email"] == "qwe@qwe.com"
        assert tmp["fullname"] == "qwe qwe"
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
                username_from_email: str = payload_token.get("sub")
            except JWTError:
                assert False
            assert username == username_from_email
            with redisdb.pipeline() as pipe:
                pipe.multi()
                pipe.get(namespase + username)
                pipe.delete(namespase + username)
                result = pipe.execute()
            assert result[1] != 0
            userdata = json.loads(result[0])
            assert userdata["fullname"] == payload["full_name"]
            userdata["email"] == "qwe@qwe.com"
            assert verify_password(payload["password"],
                                   userdata["hash_password"])


test_cases = {
    "short_password": (
        {
            "username": "qwerty",
            "password": "secret",
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe"
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
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe"
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
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe"
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
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe"
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
    "short_fullname": (
        {
            "username": "qwerty",
            "password": "supersecret",
            "email": "qwe@qwe.com",
            "full_name": "qw"
        },
        {
            "status": 422,
            "json": {
                'detail': [
                    {
                        'ctx': {'limit_value': 3},
                        'loc': ['body', 'full_name'],
                        'msg': 'ensure this value has at least 3 characters',
                        'type': 'value_error.any_str.min_length'
                    }
                ]
            }
        }
    ),
    "too_long_fullname": (
        {
            "username": "qwerty",
            "password": "supersecret",
            "email": "qwe@qwe.com",
            "full_name": "q" * 51
        },
        {
            "status": 422,
            "json": {
                'detail': [
                    {
                        'ctx': {'limit_value': 50},
                        'loc': ['body', 'full_name'],
                        'msg': 'ensure this value has at most 50 characters',
                        'type': 'value_error.any_str.max_length'
                    }
                ]
            }
        }
    )
}


@pytest.mark.parametrize("user_data,resp", test_cases.values(),
                         ids=list(test_cases.keys()))
def test_signup_validation(migrated_postgres_connection, redisdb, url,
                           user_data, resp):
    with TestClient(app, base_url=url) as client:
        response = client.post("/signup", data=user_data)
        assert response.status_code == resp["status"]
        assert response.json() == resp["json"]


test_email_cases = {
    "email_1": (
        {
            "username": "qwerty",
            "password": "supersecret",
            "email": "qwe",
            "full_name": "qwe qwe"
        },
        {
            "status": 422,
            "json": {
                'detail': [
                    {
                        'loc': ['body', 'email'],
                        'msg': 'value is not a valid email address',
                        'type': 'value_error.email'
                    }
                ]
            }
        }
    ),
    "email_2": (
        {
            "username": "qwerty",
            "password": "supersecret",
            "email": "qwe@qwe",
            "full_name": "qwe qwe"
        },
        {
            "status": 422,
            "json": {
                'detail': [
                    {
                        'loc': ['body', 'email'],
                        'msg': 'value is not a valid email address',
                        'type': 'value_error.email'
                    }
                ]
            }
        }
    )
}


@pytest.mark.parametrize("user_data,resp", test_email_cases.values(),
                         ids=list(test_email_cases.keys()))
def test_email_validation(migrated_postgres_connection, redisdb, url,
                          user_data, resp):
    with TestClient(app, base_url=url) as client:
        response = client.post("/signup", data=user_data)
        assert response.status_code == resp["status"]
        assert response.json() == resp["json"]


nonconfirmed_user_data_cases = {
    "duplicate": (
        {
            "username": "qwerty",
            "password": "supersecret",
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe"
        },
        {
            "status": 200,
            "json": {
                "operation": "signup",
                "successful": True
            }
        },
        {
            "username": "qwerty",
            "password": "supersecret",
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe"
        },
        {
            "status": 422,
            "json": {
                "detail": [
                    {
                        'loc': ['username'],
                        'msg': 'Username already exists',
                        'type': 'value_error'
                    },
                    {
                        'loc': ['email'],
                        'msg': 'Email already exists',
                        'type': 'value_error'
                    }
                ]
            }
        }
    ),
    "different_username": (
        {
            "username": "qwerty",
            "password": "supersecret",
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe"
        },
        {
            "status": 200,
            "json": {
                "operation": "signup",
                "successful": True
            }
        },
        {
            "username": "qwerty1",
            "password": "supersecret",
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe"
        },
        {
            "status": 422,
            "json": {
                "detail": [
                    {
                        'loc': ['email'],
                        'msg': 'Email already exists',
                        'type': 'value_error'
                    }
                ]
            }
        }
    ),
    "different_email": (
        {
            "username": "qwerty",
            "password": "supersecret",
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe"
        },
        {
            "status": 200,
            "json": {
                "operation": "signup",
                "successful": True
            }
        },
        {
            "username": "qwerty",
            "password": "supersecret",
            "email": "qwe1@qwe.com",
            "full_name": "qwe qwe"
        },
        {
            "status": 422,
            "json": {
                "detail": [
                    {
                        'loc': ['username'],
                        'msg': 'Username already exists',
                        'type': 'value_error'
                    }
                ]
            }
        }
    ),
    "different_password": (
        {
            "username": "qwerty",
            "password": "supersecret",
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe"
        },
        {
            "status": 200,
            "json": {
                "operation": "signup",
                "successful": True
            }
        },
        {
            "username": "qwerty",
            "password": "supersecret1",
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe"
        },
        {
            "status": 422,
            "json": {
                "detail": [
                    {
                        'loc': ['username'],
                        'msg': 'Username already exists',
                        'type': 'value_error'
                    },
                    {
                        'loc': ['email'],
                        'msg': 'Email already exists',
                        'type': 'value_error'
                    }
                ]
            }
        }
    ),
    "different_full_name": (
        {
            "username": "qwerty",
            "password": "supersecret",
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe"
        },
        {
            "status": 200,
            "json": {
                "operation": "signup",
                "successful": True
            }
        },
        {
            "username": "qwerty",
            "password": "supersecret",
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe1"
        },
        {
            "status": 422,
            "json": {
                "detail": [
                    {
                        'loc': ['username'],
                        'msg': 'Username already exists',
                        'type': 'value_error'
                    },
                    {
                        'loc': ['email'],
                        'msg': 'Email already exists',
                        'type': 'value_error'
                    }
                ]
            }
        }
    ),
    "identical_username": (
        {
            "username": "qwerty",
            "password": "supersecret",
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe"
        },
        {
            "status": 200,
            "json": {
                "operation": "signup",
                "successful": True
            }
        },
        {
            "username": "qwerty",
            "password": "supersecret1",
            "email": "qwe1@qwe.com",
            "full_name": "qwe qwe1"
        },
        {
            "status": 422,
            "json": {
                "detail": [
                    {
                        'loc': ['username'],
                        'msg': 'Username already exists',
                        'type': 'value_error'
                    }
                ]
            }
        }
    ),
    "identical_email": (
        {
            "username": "qwerty",
            "password": "supersecret",
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe"
        },
        {
            "status": 200,
            "json": {
                "operation": "signup",
                "successful": True
            }
        },
        {
            "username": "qwerty1",
            "password": "supersecret1",
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe1"
        },
        {
            "status": 422,
            "json": {
                "detail": [
                    {
                        'loc': ['email'],
                        'msg': 'Email already exists',
                        'type': 'value_error'
                    }
                ]
            }
        }
    ),
    "identical_full_name": (
        {
            "username": "qwerty",
            "password": "supersecret",
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe"
        },
        {
            "status": 200,
            "json": {
                "operation": "signup",
                "successful": True
            }
        },
        {
            "username": "qwerty1",
            "password": "supersecret1",
            "email": "qwe1@qwe.com",
            "full_name": "qwe qwe"
        },
        {
            "status": 200,
            "json": {
                "operation": "signup",
                "successful": True
            }
        }
    ),
    "identical_password": (
        {
            "username": "qwerty",
            "password": "supersecret",
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe"
        },
        {
            "status": 200,
            "json": {
                "operation": "signup",
                "successful": True
            }
        },
        {
            "username": "qwerty1",
            "password": "supersecret",
            "email": "qwe1@qwe.com",
            "full_name": "qwe qwe1"
        },
        {
            "status": 200,
            "json": {
                "operation": "signup",
                "successful": True
            }
        }
    )
}


@pytest.mark.parametrize("user_data_1,resp_1,user_data_2,resp_2",
                         nonconfirmed_user_data_cases.values(),
                         ids=list(nonconfirmed_user_data_cases.keys()))
def test_nonconfirmed_user_data(migrated_postgres_connection,
                                redisdb, url, user_data_1, resp_1,
                                user_data_2, resp_2):
    with TestClient(app, base_url=url) as client:
        response = client.post("/signup", data=user_data_1)
        assert response.status_code == resp_1["status"]
        assert response.json() == resp_1["json"]
        response = client.post("/signup", data=user_data_2)
        assert response.status_code == resp_2["status"]
        assert response.json() == resp_2["json"]


already_existed_in_db_cases = {
    "identical_user_data": (
        {
            "username": "qwerty",
            "password": "supersecret",
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe"
        },
        {
            "status": 422,
            "json": {
                "detail": [
                    {
                        'loc': ['username'],
                        'msg': 'Username already exists',
                        'type': 'value_error'
                    },
                    {
                        'loc': ['email'],
                        'msg': 'Email already exists',
                        'type': 'value_error'
                    }
                ]
            }
        }
    ),
    "identical_username": (
        {
            "username": "qwerty",
            "password": "supersecret1",
            "email": "qwe1@qwe.com",
            "full_name": "qwe qwe1"
        },
        {
            "status": 422,
            "json": {
                "detail": [
                    {
                        'loc': ['username'],
                        'msg': 'Username already exists',
                        'type': 'value_error'
                    }
                ]
            }
        }
    ),
    "identical_email": (
        {
            "username": "qwerty1",
            "password": "supersecret1",
            "email": "qwe@qwe.com",
            "full_name": "qwe qwe1"
        },
        {
            "status": 422,
            "json": {
                "detail": [
                    {
                        'loc': ['email'],
                        'msg': 'Email already exists',
                        'type': 'value_error'
                    }
                ]
            }
        }
    ),
    "identical_full_name": (
        {
            "username": "qwerty1",
            "password": "supersecret1",
            "email": "qwe1@qwe.com",
            "full_name": "qwe qwe"
        },
        {
            "status": 200,
            "json": {
                "operation": "signup",
                "successful": True
            }
        }
    ),
    "identical_password": (
        {
            "username": "qwerty1",
            "password": "supersecret",
            "email": "qwe1@qwe.com",
            "full_name": "qwe qwe1"
        },
        {
            "status": 200,
            "json": {
                "operation": "signup",
                "successful": True
            }
        }
    )
}


@pytest.mark.parametrize("user_data,resp",
                         already_existed_in_db_cases.values(),
                         ids=list(already_existed_in_db_cases.keys()))
def test_confirmed_user_data(migrated_postgres_connection, redisdb, url,
                             user_data, resp):
    migrated_postgres_connection.execute(insert_new_user(
        "qwerty", "qwe", "qwe@qwe.com", get_password_hash("supersecret")))

    with TestClient(app, base_url=url) as client:
        response = client.post("/signup", data=user_data)
        assert response.status_code == resp["status"]
        assert response.json() == resp["json"]
