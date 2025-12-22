from pydantic import BaseModel

class AssignmentCreateResponse(BaseModel):
    assignment_id: str
    filename: str
