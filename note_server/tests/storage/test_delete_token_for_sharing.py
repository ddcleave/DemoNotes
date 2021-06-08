from src.services.adapters.postgres_storage import PostgresStorage
from src.entities.note import NoteDeleteToken
from src.db.models import Note, PersonalNote


def test_delete_token_for_sharing(migrated_postgres_sessionmaker, monkeypatch):
    test_username = "qwerty4"
    data = "testdata1"
    token = "test"

    with migrated_postgres_sessionmaker() as session:
        datanote = Note(data=data, creator=test_username, token=token)
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

    for_sharing = NoteDeleteToken(
        user=test_username,
        id=pers_note.id
    )


    res = PostgresStorage(migrated_postgres_sessionmaker).delete_token_for_sharing(for_sharing)

    assert res.id == pers_note.id
    assert res.user == test_username
    assert res.note.creator == test_username
    assert res.note.data == data
    assert res.shared == False
    assert res.position == 0
    assert res.note.token == None