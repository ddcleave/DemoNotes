from pydantic.main import BaseModel


class NewNote(BaseModel):
    note: str
    tags: list[str] = []

class UpdateTag(BaseModel):
    note: str
    tag: str
