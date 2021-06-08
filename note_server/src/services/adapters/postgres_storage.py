from secrets import token_urlsafe
from typing import Optional

from sqlalchemy import create_engine, delete, insert, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import sessionmaker
from src.db.models import (Note, PersonalNote, Tag, UserMaxPosition,
                           tag_note_association_table)
from src.entities.note import (NoteCreate, NoteDelete, NoteDeleteToken,
                               NoteFilter, NoteGetItem, NoteImportToken,
                               NoteItem, NoteSetToken, NoteSwapPosition,
                               NoteUpdate, NoteUUID, TagAdd, TagCreate,
                               TagItem, TagRemove, TagsGet)
from src.services.interfaces.storage import NoteStorage
from src.db.database import Session
# engine = create_engine("postgresql://user:hackme@postgres-note:5433/note")

# Session = sessionmaker(engine)

# session = Session()


class PostgresStorage(NoteStorage):
    def __init__(self, session=None) -> None:
        if session is None:
            self.session = Session
        else:
            self.session = session

    def create_note(self, note: NoteCreate) -> NoteItem:
        with self.session() as session:
            # создаем заметку
            note_obj = Note(creator=note.creator, data=note.data)
            session.add(note_obj)
            session.commit()
            session.refresh(note_obj)
            # добавляем ее к заметкам пользователя
            # добавляем позицию к заметке
            # чтобы это сделать надо добавить запись в юзермакспозишен, если ее нет
            # если есть увеличить на 1
            stmt = pg_insert(UserMaxPosition).values(
                user=note.creator, max_pos=0)
            do_update_stmt = stmt.on_conflict_do_update(
                index_elements=['user'],
                set_=dict(max_pos=UserMaxPosition.max_pos + 1)
            ).returning(UserMaxPosition.max_pos)
            position_note = session.execute(do_update_stmt).scalar_one()
            ###########
            pers_note = PersonalNote(note_id=note_obj.id,
                                     user=note_obj.creator,
                                     shared=False,
                                     position=position_note)
            session.add(pers_note)
            session.commit()
            session.refresh(pers_note)
            # получаем ид тегов, которые уже существуют
            # all_tags = session.execute(select(Tag.id).\
            #                            where(Tag.user==note.creator).\
            #                            where(Tag.label.in_(note.tags))).scalars().all()

            # надо проверить что апсерт работает и выдает все записи
            if note.tags:
                values = [{"label": tag, "user": note.creator}
                          for tag in note.tags]
                stmt = pg_insert(Tag).values(values)
                do_update_stmt = stmt.on_conflict_do_update(
                    constraint='_label_user_uc',
                    set_=dict(label=stmt.excluded.label, user=stmt.excluded.user)
                ).returning(Tag.id)
                all_tags = session.execute(do_update_stmt).scalars().all()
                # добавляем теги к заметке
                # сделано грубым методом, надо разобраться как это решить

                # for tag in all_tags:
                #     session.execute(
                #         insert(tag_note_association_table).values(tag_id=tag,
                #         pers_note_id=pers_note.id)
                #     )
                # заменил последовательный вызов инсертов на один
                values = [{"tag_id": tag, "pers_note_id": pers_note.id}
                          for tag in all_tags]
                session.execute(insert(tag_note_association_table).values(values))

                session.commit()
            # надо определиться, что нужно вернуть
            return NoteItem.from_orm(pers_note)

    def add_tag(self, tag: TagAdd) -> NoteItem:
        with self.session() as session:
            add_tag = session.execute(
                select(Tag).where(Tag.user == tag.user).
                where(Tag.label == tag.label)
            ).scalar_one()
            query = select(PersonalNote).\
                where(PersonalNote.id == tag.pers_note_id).\
                where(PersonalNote.user == tag.user)
            note = session.execute(query).scalar_one()
            note.tags.append(add_tag)
            session.commit()
            session.refresh(note)
            return NoteItem.from_orm(note)
    
    def remove_tag(self, tag: TagRemove) -> NoteItem:
        with self.session() as session:
            note = session.execute(
                select(PersonalNote).where(PersonalNote.id == tag.note_id).
                where(PersonalNote.user == tag.user)
            ).scalar_one()
            remove_tag = session.execute(
                select(Tag).where(Tag.label == tag.label).
                where(Tag.user == tag.user)
            ).scalar_one()
            note.tags.remove(remove_tag)
            session.commit()
            session.refresh(note)
            return NoteItem.from_orm(note)

    def create_and_add_tag(self, tag: TagAdd) -> NoteItem:
        with self.session() as session:
            stmt = pg_insert(Tag).values(
                label=tag.label,
                user=tag.user)
            do_update_stmt = stmt.on_conflict_do_update(
                constraint='_label_user_uc',
                set_=dict(label=stmt.excluded.label, user=stmt.excluded.user)
            ).returning(Tag.id)
            tag_id = session.execute(do_update_stmt).scalar()
            query = select(PersonalNote.id).\
                where(PersonalNote.id == tag.pers_note_id).\
                where(PersonalNote.user == tag.user)
            check_pers_note_id = session.execute(query).fetchone()
            if check_pers_note_id:
                session.execute(
                    insert(tag_note_association_table).
                    values(tag_id=tag_id,
                           pers_note_id=tag.pers_note_id)
                )
                session.commit()
            query = select(PersonalNote).\
                where(PersonalNote.id == tag.pers_note_id).\
                where(PersonalNote.user == tag.user)
            res_note = session.execute(query).fetchone()
            session.commit()
            return NoteItem.from_orm(res_note[0])

    def create_tag(self, tag: TagCreate) -> TagItem:
        with self.session() as session:
            stmt = pg_insert(Tag).values(
                label=tag.label,
                user=tag.user)
            do_update_stmt = stmt.on_conflict_do_update(
                constraint='_label_user_uc',
                set_=dict(label=stmt.excluded.label, user=stmt.excluded.user)
            ).returning(Tag.label)
            created_tag_label = session.execute(do_update_stmt).scalar_one()
            session.commit()
            return TagItem(label=created_tag_label)

    def get_note(self, note: NoteGetItem) -> NoteItem:
        with self.session() as session:
            note_item = session.execute(
                select(PersonalNote).where(PersonalNote.id == note.id).
                where(PersonalNote.user == note.user)
            ).scalar_one()
            return NoteItem.from_orm(note_item)

    def update_note(self, note: NoteUpdate) -> NoteItem:
        with self.session() as session:
            updated_note = session.execute(
                select(PersonalNote).where(PersonalNote.user == note.user).
                where(PersonalNote.id == note.id)
            ).scalar_one()
            updated_note.note.data = note.data
            session.commit()
            return NoteItem.from_orm(updated_note)

    def delete_note(self, note: NoteDelete) -> NoteUUID:
        with self.session() as session:
            deleted_note = session.execute(
                select(PersonalNote).where(PersonalNote.user == note.user).
                where(PersonalNote.id == note.id)
            ).scalar()
            if deleted_note:
                # session.execute(
                #     delete(tag_note_association_table).\
                #     where(tag_note_association_table.c.pers_note_id == note.id)
                # )
                deleted_note.tags[:] = []
                if not deleted_note.shared:
                    session.execute(
                        delete(PersonalNote).
                        where(PersonalNote.note_id == deleted_note.note_id)
                    )
                    session.execute(
                        update(PersonalNote).
                        where(PersonalNote.note_id == deleted_note.note_id).
                        where(PersonalNote.id != deleted_note.id).
                        values(note_id=None)
                    )
                else:
                    session.delete(deleted_note)
                session.commit()
                return NoteUUID(id=deleted_note.id)
            return NoteUUID(id=None)
        # deleted_note_id = session.execute(
        #     delete(PersonalNote).where(PersonalNote.user==note.user).\
        #         where(PersonalNote.id==note.id).returning(PersonalNote.id)
        # ).scalar_one()
        # print(deleted_note_id)
        # todo решить проблему с удаление Note

    def get_notes(self, filter: NoteFilter) -> list[NoteItem]:
        with self.session() as session:
            stmt = select(PersonalNote).where(PersonalNote.user == filter.user).\
                order_by(PersonalNote.position.desc()).\
                limit(10)
            
            if filter.position != None:
                stmt = stmt.where(PersonalNote.position < filter.position)
            if filter.tag != None:
                stmt = stmt.join(Tag, PersonalNote.tags).\
                    where(Tag.label == filter.tag)
                
            notes = session.execute(stmt).scalars().all()
            # if filter.position != None:
            #     notes = session.execute(
            #         stmt.where(PersonalNote.position < filter.position)
            #     ).scalars().all()
            # else:
            #     notes = session.execute(stmt).scalars().all()
            return [NoteItem.from_orm(note) for note in notes]

    def swap_notes(self, notes: NoteSwapPosition) -> list[NoteItem]:
        with self.session() as session:
            first_note = session.execute(
                select(PersonalNote).where(PersonalNote.user == notes.user).
                where(PersonalNote.id == notes.first_note_id)
            ).scalar()
            second_note = session.execute(
                select(PersonalNote).where(PersonalNote.user == notes.user).
                where(PersonalNote.id == notes.second_note_id)
            ).scalar()
            if first_note != None and second_note != None:
                first_note.position, second_note.position =\
                    second_note.position, first_note.position
                session.commit()
                return [NoteItem.from_orm(first_note),
                        NoteItem.from_orm(second_note)]
            return []

    def set_token_for_sharing(
            self, note_for_set_token: NoteSetToken) -> Optional[NoteItem]:
        with self.session() as session:
            note = session.execute(
                select(PersonalNote).where(PersonalNote.user == note_for_set_token.user).
                where(PersonalNote.id == note_for_set_token.id)
            ).scalar()
            if note:
                if note.user == note.note.creator:
                    note.note.token = token_urlsafe(16)
                    session.commit()
                    session.refresh(note)
                return NoteItem.from_orm(note)
            return None

    def delete_token_for_sharing(
        self, note_for_delete_token: NoteDeleteToken) -> Optional[NoteItem]:
        with self.session() as session:
            note = session.execute(
                select(PersonalNote).where(PersonalNote.user == note_for_delete_token.user).
                where(PersonalNote.id == note_for_delete_token.id)
            ).scalar()
            if note:
                if note.user == note.note.creator:
                    note.note.token = None
                    session.commit()
                    session.refresh(note)
                return NoteItem.from_orm(note)
            return None

    def import_note(self, import_note: NoteImportToken) -> Optional[NoteItem]:
        with self.session() as session:
            data_note = session.execute(
                select(Note).where(Note.token==import_note.token)
            ).scalar()
            if data_note:
                stmt = pg_insert(UserMaxPosition).values(
                    user=import_note.user, max_pos=0)
                do_update_stmt = stmt.on_conflict_do_update(
                    index_elements=['user'],
                    set_=dict(max_pos=UserMaxPosition.max_pos + 1)
                ).returning(UserMaxPosition.max_pos)
                position_note = session.execute(do_update_stmt).scalar_one()

                pers_note = PersonalNote(note_id=data_note.id,
                                         user=import_note.user,
                                         shared=True,
                                         position=position_note)

                session.add(pers_note)
                session.commit()
                session.refresh(pers_note)
                return NoteItem.from_orm(pers_note)
            return None
    
    def get_tags(self, to_get_tags: TagsGet) -> list[TagItem]:
        with self.session() as session:
            all_tags = session.execute(
                select(Tag).where(Tag.user == to_get_tags.user)
            ).scalars().all()
            return [TagItem.from_orm(tag) for tag in all_tags]
