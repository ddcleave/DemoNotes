from .base_usecase import BaseUseCase
from src.entities.note import TagCreate, TagItem


class CreateTag(BaseUseCase):
    def execute(self, tag: TagCreate) -> TagItem:
        tag_obj = self.repo.create_tag(tag)
        return tag_obj