from .base_usecase import BaseUseCase
from src.entities.note import TagRemove, NoteItem


class RemoveTag(BaseUseCase):
    def execute(self, tag: TagRemove) -> NoteItem:
        note_obj = self.repo.remove_tag(tag)
        return note_obj