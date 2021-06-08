from sqlalchemy import select
from src.db.models import Tag
from src.entities.note import TagCreate
from src.services.adapters.postgres_storage import PostgresStorage
from sqlalchemy import insert


def test_create_tag(migrated_postgres_sessionmaker):
    test_username = "qwerty4"

    tag = TagCreate(
        user=test_username,
        label="KEKW"
    )
    res = PostgresStorage(migrated_postgres_sessionmaker).create_tag(tag)
    
    assert res.label == "KEKW"
