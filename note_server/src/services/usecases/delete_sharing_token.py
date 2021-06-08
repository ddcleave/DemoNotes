from typing import Optional
from .base_usecase import BaseUseCase
from src.entities.note import NoteDeleteToken, NoteItem


class DeleteSharingToken(BaseUseCase):
    def execute(self, delete_code: NoteDeleteToken) -> Optional[NoteItem]:
        export_record_obj = self.repo.delete_token_for_sharing(delete_code)
        return export_record_obj