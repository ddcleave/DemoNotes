from .base_usecase import BaseUseCase
from src.entities.note import NoteDelete, NoteItem


class DeleteNote(BaseUseCase):
    def execute(self, note: NoteDelete) -> NoteItem:
        note_obj = self.repo.delete_note(note)
        return note_obj