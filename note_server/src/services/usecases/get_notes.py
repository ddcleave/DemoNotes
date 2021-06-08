from .base_usecase import BaseUseCase
from src.entities.note import NoteFilter, NoteItem


class GetNotes(BaseUseCase):
    def execute(self, filter: NoteFilter) -> list[NoteItem]:
        list_notes = self.repo.get_notes(filter)
        return list_notes