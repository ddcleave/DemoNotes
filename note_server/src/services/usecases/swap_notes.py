from .base_usecase import BaseUseCase
from src.entities.note import NoteSwapPosition, NoteItem


class SwapNotes(BaseUseCase):
    def execute(self, notes: NoteSwapPosition) -> list[NoteItem]:
        list_notes = self.repo.swap_notes(notes)
        return list_notes