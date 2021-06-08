from src.services.adapters.postgres_storage import PostgresStorage
from src.entities.note import NoteUpdate
from src.db.models import Note, PersonalNote


def test_update_note(migrated_postgres_sessionmaker):
    test_username = "qwerty4"
    data = "testdata1"
    data_for_update = "testdata2"

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

    update_note = NoteUpdate(
        user=test_username,
        id=pers_note.id,
        data=data_for_update
    )

    res = PostgresStorage(migrated_postgres_sessionmaker).update_note(update_note)

    assert res.id == pers_note.id
    assert res.user == test_username
    assert res.note.creator == test_username
    assert res.note.data == data_for_update
    assert res.shared == False
    assert res.position == 0