from src.services.adapters.postgres_storage import PostgresStorage
from src.entities.note import NoteImportToken, NoteSetToken
from src.db.models import Note, PersonalNote


def test_import_note(migrated_postgres_sessionmaker, monkeypatch):
    test_creator = "qwerty"
    test_username = "qwerty4"
    data = "testdata1"

    with migrated_postgres_sessionmaker() as session:
        datanote = Note(data=data, creator=test_creator, token="test")
        session.add(datanote)
        session.commit()
        session.refresh(datanote)

        pers_note = PersonalNote(
            user=test_creator,
            shared=False,
            note=datanote,
            position=0
        )
        session.add(pers_note)
        session.commit()
        session.refresh(pers_note)

        import_note = NoteImportToken(
            user=test_username,
            token="test"
        )

    res = PostgresStorage(migrated_postgres_sessionmaker).import_note(import_note)

    assert res.id != pers_note.id
    assert res.user == test_username
    assert res.note.creator == test_creator
    assert res.note.data == data
    assert res.shared == True
    assert res.position == 0
    assert res.note.token == "test"