from .base_usecase import BaseUseCase
from src.entities.note import TagsGet, TagItem


class GetTags(BaseUseCase):
    def execute(self, to_get_tags: TagsGet) -> list[TagItem]:
        all_tags = self.repo.get_tags(to_get_tags)
        return all_tags