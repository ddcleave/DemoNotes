from uuid import uuid4
from sqlalchemy import select
from src.services.adapters.postgres_storage import PostgresStorage
from src.entities.note import NoteDelete, NoteUpdate
from src.db.models import Note, PersonalNote, Tag
from sqlalchemy.dialects.postgresql import insert as pg_insert


def test_delete_note(migrated_postgres_sessionmaker):
    test_username = "qwerty4"
    data = "testdata1"
    with migrated_postgres_sessionmaker() as session:
        datanote = Note(data=data, creator=test_username)
        session.add(datanote)
        session.commit()
        session.refresh(datanote)

        pers_note = PersonalNote(
            user=test_username,
            shared=False,
            note=datanote,
            position=0
        )
        session.add(pers_note)
        session.commit()
        session.refresh(pers_note)

    note_for_delete = NoteDelete(
        user=test_username,
        id=pers_note.id
    )

    res = PostgresStorage(migrated_postgres_sessionmaker).delete_note(note_for_delete)
    assert res.id == pers_note.id

    with migrated_postgres_sessionmaker() as session:
        check_note = session.execute(
            select(PersonalNote).where(PersonalNote.user==test_username).\
                where(PersonalNote.id==pers_note.id)
        ).all()
        assert check_note == []


def test_delete_not_existed_note(migrated_postgres_sessionmaker):
    test_username = "qwerty4"
    data = "testdata1"

    note_for_delete = NoteDelete(
        user=test_username,
        id=uuid4()
    )

    res = PostgresStorage(migrated_postgres_sessionmaker).delete_note(note_for_delete)

    assert res.id == None


def test_delete_note_with_tags(migrated_postgres_sessionmaker):
    test_username = "qwerty4"
    data = "testdata1"
    with migrated_postgres_sessionmaker() as session:
        datanote = Note(data=data, creator=test_username)
        session.add(datanote)
        session.commit()
        session.refresh(datanote)

        pers_note = PersonalNote(
            user=test_username,
            shared=False,
            note=datanote,
            position=0
        )
        session.add(pers_note)
        session.commit()

        session.refresh(pers_note)

        tag = Tag(label="KEKW", user=test_username)

        pers_note.tags.append(tag)

        session.commit()


        note_for_delete = NoteDelete(
            user=test_username,
            id=pers_note.id
        )

        res = PostgresStorage(migrated_postgres_sessionmaker).delete_note(note_for_delete)

        assert res.id == pers_note.id
        check_note = session.execute(
            select(PersonalNote).where(PersonalNote.user==test_username).\
                where(PersonalNote.id==pers_note.id)
        ).all()
        assert check_note == []