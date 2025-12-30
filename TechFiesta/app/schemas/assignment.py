from pydantic import BaseModel


class AssignmentCreateResponse(BaseModel):
    assignment_id: str
    filename: str
    total_sentences: int
    preview_sentences: list[str]
