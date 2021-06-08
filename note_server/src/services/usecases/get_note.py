from .base_usecase import BaseUseCase
from src.entities.note import NoteGetItem, NoteItem


class GetNote(BaseUseCase):
    def execute(self, note: NoteGetItem) -> NoteItem:
        note_obj = self.repo.get_note(note)
        return note_obj