from sqlalchemy import (Column, DateTime, ForeignKey, Identity, Integer,
                        String, Table, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


Base = declarative_base()


tag_note_association_table = Table('tag_note_association', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
    Column('pers_note_id', UUID(as_uuid=True),
           ForeignKey('personal_notes.id'), primary_key=True)
)


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, Identity(), primary_key=True)
    data = Column(String)
    create_date = Column(DateTime, server_default=func.now())
    creator = Column(String, nullable=False)
    token = Column(String)

    __mapper_args__ = {"eager_defaults": True}


class ShareNote(Base):
    __tablename__ = "share_notes"

    id = Column(Integer, Identity(), primary_key=True)
    note_id = Column(Integer, ForeignKey("notes.id"), nullable=False)
    sync = Column(Boolean, nullable=False)
    link = Column(String)



class PersonalNote(Base):
    __tablename__ = "personal_notes"

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid4)
    user = Column(String, nullable=False, index=True)
    shared = Column(Boolean, nullable=False)
    note_id = Column(Integer, ForeignKey("notes.id"))
    position = Column(Integer, nullable=False, index=True)

    tags = relationship(
        "Tag",
        secondary=tag_note_association_table,
        backref=backref("pers_notes", lazy=True)
        )
    note = relationship("Note", foreign_keys=[note_id])


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, Identity(), primary_key=True)
    label = Column(String, nullable=False)
    user = Column(String, nullable=False, index=True)

    __table_args__ = (UniqueConstraint('label','user',
                                       name='_label_user_uc'),)


class UserMaxPosition(Base):
    __tablename__ = "users_max_position"

    user = Column(String, primary_key=True)
    max_pos = Column(Integer, nullable=False)
