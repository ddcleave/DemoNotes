# добавить


from src.entities.note import TagsGet
from src.services.adapters.postgres_storage import PostgresStorage
from src.db.models import Tag


def test_get_tags(migrated_postgres_sessionmaker):
    test_username = "qwerty4"
    tag_label_list = ["test1", "test2", "test3"]

    with migrated_postgres_sessionmaker() as session:
        tag_list = [Tag(label=tag_label, user=test_username) \
                    for tag_label in tag_label_list]
        session.add_all(tag_list)
        session.commit()

    tags_get = TagsGet(user=test_username)

    res = PostgresStorage(migrated_postgres_sessionmaker).get_tags(tags_get)
    
    assert len(res) == len(tag_label_list)
    assert set((i.label for i in res)) == set(tag_label_list)
