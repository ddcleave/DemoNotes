from .base_usecase import BaseUseCase
from src.entities.note import NoteImportToken, NoteItem


class ImportNote(BaseUseCase):
    def execute(self, link: NoteImportToken) -> NoteItem:
        note_obj = self.repo.import_note(link)
        return note_obj