from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.utils.alembic import make_alembic_config
from sqlalchemy_utils import create_database, drop_database
import pytest
from alembic.command import upgrade


@pytest.fixture
def postgres():
    postgres_url = "postgresql://user:hackme@localhost:5433/pytest"
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
def migrated_postgres(alembic_config, postgres):
    upgrade(alembic_config, 'head')
    return postgres

@pytest.fixture
def migrated_postgres_session(migrated_postgres):
    engine = create_engine(migrated_postgres)
    Session = sessionmaker(engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()

@pytest.fixture
def migrated_postgres_sessionmaker(migrated_postgres):
    engine = create_engine(migrated_postgres)
    Session = sessionmaker(engine)
    try:
        yield Session
    finally:
        engine.dispose()