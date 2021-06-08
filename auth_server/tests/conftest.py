import pytest
from sqlalchemy_utils import create_database, drop_database
from auth_server.core.config import get_settings
from alembic.command import upgrade
from auth_server.services.alembic import make_alembic_config
from sqlalchemy import create_engine
from redis import from_url


@pytest.fixture
def postgres():
    postgres_url = get_settings().test_database_url
    create_database(postgres_url)

    try:
        yield postgres_url
    finally:
        drop_database(postgres_url)


@pytest.fixture
def alembic_config(postgres):
    return make_alembic_config(config_file="alembic-dev.ini",
                               ini_section="alembic",
                               pg_url=postgres)


@pytest.fixture
async def migrated_postgres(alembic_config, postgres):
    upgrade(alembic_config, 'head')
    return postgres


@pytest.fixture
def migrated_postgres_connection(migrated_postgres):
    engine = create_engine(migrated_postgres)
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()
        engine.dispose()


@pytest.fixture
def redisdb():
    redis_db = from_url(url=get_settings().test_redis_url)
    yield redis_db
    redis_db.flushdb()
