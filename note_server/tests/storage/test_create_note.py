from src.db.models import PersonalNote, Tag
from src.entities.note import NoteCreate, NoteItem
from src.services.adapters.postgres_storage import PostgresStorage
from sqlalchemy import insert


def test_basic(migrated_postgres_sessionmaker):
    test_username = "qwerty4"
    data = "testdata1"
    tags = ["KEKW","LUL"]
    note = NoteCreate(
        creator=test_username,
        data=data,
        tags=tags)
    res = PostgresStorage(migrated_postgres_sessionmaker).create_note(note)
    
    assert res.id != None
    assert res.user == test_username
    assert res.note.creator == test_username
    assert res.note.data == data
    assert res.shared == False
    assert res.position == 0
    assert len(res.tags) == len(tags)
    for tag_db, tag_test in zip(res.tags, tags):
        assert tag_db.label == tag_test

def test_no_tags_explicit(migrated_postgres_sessionmaker):
    test_username = "qwerty4"
    data = "testdata1"
    tags = []
    note = NoteCreate(
        creator=test_username,
        data=data,
        tags=tags)
    res = PostgresStorage(migrated_postgres_sessionmaker).create_note(note)
    
    assert res.id != None
    assert res.user == test_username
    assert res.note.creator == test_username
    assert res.note.data == data
    assert res.shared == False
    assert res.position == 0
    assert res.tags == []


def test_no_tags_explicit2(migrated_postgres_sessionmaker):
    test_username = "qwerty4"
    data = "testdata1"
    note = NoteCreate(
        creator=test_username,
        data=data)
    res = PostgresStorage(migrated_postgres_sessionmaker).create_note(note)
    
    assert res.id != None
    assert res.user == test_username
    assert res.note.creator == test_username
    assert res.note.data == data
    assert res.shared == False
    assert res.position == 0
    assert res.tags == []

def test_with_existing_tag(migrated_postgres_sessionmaker):
    test_username = "qwerty4"
    data = "testdata1"
    tags = ["KEKW","LUL"]
    note = NoteCreate(
        creator=test_username,
        data=data,
        tags=tags)

    stmt = insert(Tag).values(
        label="KEKW",
        user=test_username
    )
    with migrated_postgres_sessionmaker() as session:
        session.execute(stmt)
        session.commit()

    res = PostgresStorage(migrated_postgres_sessionmaker).create_note(note)
    
    assert res.id != None
    assert res.user == test_username
    assert res.note.creator == test_username
    assert res.note.data == data
    assert res.shared == False
    assert res.position == 0
    assert len(res.tags) == len(tags)
    for tag_db, tag_test in zip(res.tags, tags):
        assert tag_db.label == tag_test