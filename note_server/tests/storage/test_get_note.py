from src.services.adapters.postgres_storage import PostgresStorage
from src.entities.note import NoteGetItem
from src.db.models import Note, PersonalNote


def test_get_note(migrated_postgres_sessionmaker):
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

        getnote = NoteGetItem(
            user=test_username,
            id=pers_note.id
        )

    res = PostgresStorage(migrated_postgres_sessionmaker).get_note(getnote)
    
    assert res.id != None
    assert res.user == test_username
    assert res.note.creator == test_username
    assert res.note.data == data
    assert res.shared == False
    assert res.position == 0
    # assert len(res.tags) == 1
    # for tag_db, tag_test in zip(res.tags, ["KEKW"]):
    #     assert tag_db.label == tag_test
