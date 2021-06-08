from typing import Optional
from .base_usecase import BaseUseCase
from src.entities.note import NoteSetToken, NoteItem


class CreateSharingToken(BaseUseCase):
    def execute(self, set_code: NoteSetToken) -> Optional[NoteItem]:
        export_record_obj = self.repo.set_token_for_sharing(set_code)
        return export_record_obj