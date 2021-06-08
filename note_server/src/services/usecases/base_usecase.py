from src.services.interfaces.storage import NoteStorage


class BaseUseCase:
    def __init__(self, repo: NoteStorage) -> None:
        self.repo = repo