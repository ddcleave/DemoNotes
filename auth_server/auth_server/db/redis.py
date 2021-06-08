from redis import from_url
from auth_server.core.config import get_settings


if get_settings().testing:
    redis_db = from_url(url=get_settings().test_redis_url,
                        decode_responses=True)
else:
    redis_db = from_url(url=get_settings().redis_url,
                        decode_responses=True)
