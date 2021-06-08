from sqlalchemy.sql.functions import user
from src.db.models import Note, PersonalNote, Tag, tag_note_association_table
from src.entities.note import NoteCreate, NoteItem, TagAdd
from src.services.adapters.postgres_storage import PostgresStorage
from sqlalchemy import insert


def test_add_tag(migrated_postgres_sessionmaker):
    test_username = "qwerty4"
    data = "testdata1"

    stmt_create_tag = insert(Tag).values(
        label="KEKW",
        user=test_username
    )
    with migrated_postgres_sessionmaker() as session:
        session.execute(stmt_create_tag)

        stmt_create_note_data = insert(Note).values(
            data=data,
            creator=test_username
        ).returning(Note.id)
        note_id = session.execute(
            stmt_create_note_data).scalar_one()

        stmt_create_pers_note = insert(PersonalNote).values(
            user=test_username,
            shared=False,
            note_id=note_id,
            position=0
        ).returning(PersonalNote.id)
        note_uuid = session.execute(stmt_create_pers_note).scalar_one()

        tag = TagAdd(
            pers_note_id=note_uuid,
            user=test_username,
            label="KEKW"
        )
        session.commit()

    res = PostgresStorage(migrated_postgres_sessionmaker).add_tag(tag)
    
    assert res.id != None
    assert res.user == test_username
    assert res.note.creator == test_username
    assert res.note.data == data
    assert res.shared == False
    assert res.position == 0
    assert len(res.tags) == 1
    for tag_db, tag_test in zip(res.tags, ["KEKW"]):
        assert tag_db.label == tag_test

def test_add_if_already_exists(migrated_postgres_sessionmaker):
    test_username = "qwerty4"
    data = "testdata1"
    # tags = ["KEKW","LUL"]
    # note = NoteCreate(
    #     creator=test_username,
    #     data=data,
    #     tags=tags)
    with migrated_postgres_sessionmaker() as session:
        stmt_create_tag = insert(Tag).values(
            label="KEKW",
            user=test_username
        ).returning(Tag.id)
        tag_id = session.execute(stmt_create_tag).scalar_one()

        stmt_create_note_data = insert(Note).values(
            data=data,
            creator=test_username
        ).returning(Note.id)
        note_id = session.execute(
            stmt_create_note_data).scalar_one()

        stmt_create_pers_note = insert(PersonalNote).values(
            user=test_username,
            shared=False,
            note_id=note_id,
            position=0
        ).returning(PersonalNote.id)
        note_uuid = session.execute(stmt_create_pers_note).scalar_one()

        tag = TagAdd(
            pers_note_id=note_uuid,
            user=test_username,
            label="KEKW"
        )

        session.execute(
            insert(tag_note_association_table).values(
                tag_id=tag_id,
                pers_note_id=note_uuid
            )
        )

        session.commit()

    res = PostgresStorage(migrated_postgres_sessionmaker).add_tag(tag)
    
    assert res.id != None
    assert res.user == test_username
    assert res.note.creator == test_username
    assert res.note.data == data
    assert res.shared == False
    assert res.position == 0
    assert len(res.tags) == 1
    for tag_db, tag_test in zip(res.tags, ["KEKW"]):
        assert tag_db.label == tag_test