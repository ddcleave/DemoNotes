from .base_usecase import BaseUseCase
from src.entities.note import TagAdd, NoteItem


class AddTag(BaseUseCase):
    def execute(self, tag: TagAdd) -> NoteItem:
        note_obj = self.repo.add_tag(tag)
        return note_obj