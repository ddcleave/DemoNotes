import databases
from auth_server.core.config import get_settings


if get_settings().testing:
    database = databases.Database(get_settings().test_database_url)
else:
    database = databases.Database(get_settings().database_url)
