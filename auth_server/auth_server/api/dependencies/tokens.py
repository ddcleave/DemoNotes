import json
from datetime import timedelta
from uuid import uuid4

from auth_server.core.config import Settings  # это надо переделать
from auth_server.db.redis import redis_db
from auth_server.services.jwt import create_jwt_token
from fastapi import Response


async def create_and_set_tokens(username: str,
                                fingerprint: str,
                                ip: str,
                                response: Response,
                                settings: Settings,
                                ):
    # create tokens
    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)
    access_token = create_jwt_token(
        data={
            "sub": username,
            "scope": "user"
        },
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        expires_delta=access_token_expires
    )
    refresh_token = uuid4()
    r_token_dict = {
        "username": username,
        "fingerprint": fingerprint,
        "ip": ip
    }
    str_r_token = str(refresh_token)
    refresh_token_expires_seconds = settings.refresh_token_expire_days*3600*24
    # check fingerprint in redis
    namespase_all_r_tokens_of_user = "rt_user:"
    # with redis_db.pipeline() as pipe:
    #     pipe.multi()
    #     # pipe.hset(namespase_all_r_tokens_of_user + username,
    #     #           fingerprint,
    #     #           str_r_token)
    #     pipe.hkeys(namespase_all_r_tokens_of_user + username)
    #     result = pipe.execute()
    res = redis_db.hlen(namespase_all_r_tokens_of_user + username)
    # fingerprints = result[0]
    namespase = "r_token:"
    if res <= 6:
        redis_db.hset(namespase_all_r_tokens_of_user + username,
                      fingerprint,
                      str_r_token)
    else:
        tokens = redis_db.hvals(namespase_all_r_tokens_of_user + username)

        with redis_db.pipeline() as pipe:
            pipe.delete(namespase_all_r_tokens_of_user + username)
            pipe.hset(namespase_all_r_tokens_of_user + username,
                      fingerprint,
                      str_r_token)
            for i in tokens:
                pipe.delete(namespase + i)
            pipe.execute()
    # save refresh token to redis

    with redis_db.pipeline() as pipe:
        pipe.multi()
        pipe.set(namespase + str_r_token, json.dumps(r_token_dict))
        pipe.expire(namespase + str_r_token, refresh_token_expires_seconds)
        pipe.execute()
    # set cookies
    access_token_expires_seconds = settings.access_token_expire_minutes * 60
    response.set_cookie(key="access_token",
                        value=access_token,
                        domain=settings.domain,
                        max_age=access_token_expires_seconds,
                        expires=access_token_expires_seconds,
                        httponly=True,
                        # secure=True,
                        # samesite="strict"
                        )
    refresh_token_expires_seconds = settings.refresh_token_expire_days*3600*24
    response.set_cookie(key="refresh_token",
                        value=str(refresh_token),
                        max_age=refresh_token_expires_seconds,
                        expires=refresh_token_expires_seconds,
                        domain=settings.domain,
                        httponly=True,
                        # secure=True,
                        # samesite="strict"
                        )


def delete_all_refresh_tokens(user: str):
    namespace = "r_token:"
    namespase_all_r_tokens_of_user = "rt_user"
    tokens = redis_db.hvals(namespase_all_r_tokens_of_user + user)
    for token in tokens:
        redis_db.delete(namespace + token)
    redis_db.delete(namespase_all_r_tokens_of_user + user)


def invalidate_tokens(username: str, refresh_token: str,
                      response: Response, settings: Settings):
    namespace = "r_token:"
    namespase_all_r_tokens_of_user = "rt_user"
    redis_db.delete(namespace + refresh_token)
    redis_db.hdel(namespase_all_r_tokens_of_user + username, refresh_token)
    response.delete_cookie(key="access_token", domain=settings.domain)
    response.delete_cookie("refresh_token", domain=settings.domain)
