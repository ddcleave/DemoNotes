from .base_usecase import BaseUseCase
from src.entities.note import NoteCreate, NoteItem

class CreateNote(BaseUseCase):
    def execute(self, note: NoteCreate) -> NoteItem:
        note_obj = self.repo.create_note(note)
        return note_obj