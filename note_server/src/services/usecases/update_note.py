from .base_usecase import BaseUseCase
from src.entities.note import NoteUpdate, NoteItem


class UpdateNote(BaseUseCase):
    def execute(self, note: NoteUpdate) -> NoteItem:
        note_obj = self.repo.update_note(note)
        return note_obj