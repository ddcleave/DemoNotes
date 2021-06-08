from src.services.adapters.postgres_storage import PostgresStorage
from src.entities.note import NoteSwapPosition
from src.db.models import Note, PersonalNote


# переделать
def test_get_note(migrated_postgres_sessionmaker):
    test_username = "qwerty4"
    data_default = "testdata"
    notes_position = []
    notes_id = []
    with migrated_postgres_sessionmaker() as session:
        for i in range(2):
            data = data_default + str(i)
            datanote = Note(data=data, creator=test_username)
            session.add(datanote)
            session.commit()
            session.refresh(datanote)

            pers_note = PersonalNote(
                user=test_username,
                shared=False,
                note=datanote,
                position=i
            )
            session.add(pers_note)
            session.commit()
            session.refresh(pers_note)

            notes_position.append(pers_note.position)
            notes_id.append(pers_note.id)


        swap = NoteSwapPosition(
            user = test_username,
            first_note_id=notes_id[0],
            second_note_id=notes_id[1]
        )


    res = PostgresStorage(migrated_postgres_sessionmaker).swap_notes(swap)

    for i in res:
        print(i.position)

    assert res[0].id == notes_id[0]
    assert res[1].id == notes_id[1]
    assert res[0].position == notes_position[1]
    assert res[1].position == notes_position[0]
    