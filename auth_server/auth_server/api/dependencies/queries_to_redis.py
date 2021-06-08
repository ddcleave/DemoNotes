import json
from typing import Optional

from auth_server.db.redis import redis_db


def set_if_not_exist_username_and_email(username: str, email: str,
                                        exp: int) -> bool:
    namespace_name = "name:"
    namespace_email = "email:"
    with redis_db.pipeline() as pipe:
        pipe.multi()
        pipe.setnx(namespace_name + username, 0)
        pipe.expire(namespace_name + username, exp)
        pipe.setnx(namespace_email + email, 0)
        pipe.expire(namespace_email + email, exp)
        result = pipe.execute()
    if result[0] == 0 or result[2] == 0:
        return False
    return True


def set_username_and_email(username: str, email: str, exp: int) -> None:
    namespace_name = "name:"
    namespace_email = "email:"
    with redis_db.pipeline() as pipe:
        pipe.multi()
        pipe.set(namespace_name + username, 0)
        pipe.expire(namespace_name + username, exp)
        pipe.set(namespace_email + email, 0)
        pipe.expire(namespace_email + email, exp)
        pipe.execute()


def save_user_to_redis(username: str, fullname: str,
                       email: str, hash_password: str, exp: int) -> None:
    data = {
        "fullname": fullname,
        "email": email,
        "hash_password": hash_password
    }
    namespase = "userdata:"
    with redis_db.pipeline() as pipe:
        pipe.multi()
        pipe.set(namespase + username, json.dumps(data))
        pipe.expire(namespase + username, exp)
        pipe.execute()


def get_userdata(username: str) -> Optional[dict]:
    namespase = "userdata:"
    with redis_db.pipeline() as pipe:
        pipe.multi()
        pipe.get(namespase + username)
        pipe.delete(namespase + username)
        result = pipe.execute()
    if result[1] == 0:
        return None
    return {**json.loads(result[0]), "username": username}


def exist_username(username: str):
    namespace_name = "name:"
    return redis_db.exists(namespace_name + username)


def exist_email(email: str):
    namespace_email = "email:"
    return redis_db.exists(namespace_email + email)
