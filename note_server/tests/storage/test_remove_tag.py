from src.db.models import Note, PersonalNote, Tag
from sqlalchemy.sql.expression import label
from src.entities.note import NoteCreate, TagRemove
from src.services.adapters.postgres_storage import PostgresStorage


# переделать
def test_remove_tag(migrated_postgres_sessionmaker):
    test_username = "qwerty4"
    data = "testdata1"
    tags = ["KEKW","LUL"]
    with migrated_postgres_sessionmaker() as session:
        tags_items = [Tag(label=label, user=test_username) for label in tags]
        session.add_all(tags_items)
        session.commit()
        
        datanote = Note(data=data, creator=test_username)
        session.add(datanote)
        
        pers_note = PersonalNote(
            user=test_username,
            shared=False,
            note=datanote,
            position=0
        )
        for tag in tags_items:
            pers_note.tags.append(tag)
        session.add(pers_note)
        session.commit()
        session.refresh(pers_note)
    
    tag_for_remove = TagRemove(
        label="KEKW",
        user=test_username,
        note_id=pers_note.id
    )

    tmp = PostgresStorage(migrated_postgres_sessionmaker).remove_tag(tag_for_remove)

    assert len(tmp.tags) == 1
    assert tmp.tags[0].label == "LUL"