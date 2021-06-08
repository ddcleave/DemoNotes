from src.entities.note import NoteFilter
from src.services.adapters.postgres_storage import PostgresStorage

from src.db.models import Note, PersonalNote

# добавить случай с позишен = 0
# переделать
def test_get_notes(migrated_postgres_sessionmaker):
    test_username = "qwerty4"
    data_default = "testdata"
    notes = []
    with migrated_postgres_sessionmaker() as session:
        for i in range(25):
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

            notes.append(pers_note)

        filter = NoteFilter(
            user=test_username,
            position=None,
            tag=None
        )


        res = PostgresStorage(migrated_postgres_sessionmaker).get_notes(filter)

        for i in res:
        
            assert i.id != None
            assert i.user == test_username
            assert i.note.creator == test_username
            assert i.note.data == data_default + str(i.position)
            assert i.shared == False
            # assert i.position == 0


        filter = NoteFilter(
            user=test_username,
            position=7,
            tag=None
        )


        res = PostgresStorage(migrated_postgres_sessionmaker).get_notes(filter)

        assert len(res) == 7

        for i in res:
        
            assert i.id != None
            assert i.user == test_username
            assert i.note.creator == test_username
            assert i.note.data == data_default + str(i.position)
            assert i.shared == False
            # assert i.position == 0