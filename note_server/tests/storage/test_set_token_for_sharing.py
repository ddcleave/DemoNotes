from src.services.adapters.postgres_storage import PostgresStorage
from src.entities.note import NoteSetToken
from src.db.models import Note, PersonalNote


def test_set_token_for_sharing(migrated_postgres_sessionmaker, monkeypatch):
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

    for_sharing = NoteSetToken(
        user=test_username,
        id=pers_note.id
    )

    monkeypatch.setattr('src.services.adapters.postgres_storage.token_urlsafe', lambda x: "test")
    res = PostgresStorage(migrated_postgres_sessionmaker).set_token_for_sharing(for_sharing)

    assert res.id == pers_note.id
    assert res.user == test_username
    assert res.note.creator == test_username
    assert res.note.data == data
    assert res.shared == False
    assert res.position == 0
    assert res.note.token == "test"