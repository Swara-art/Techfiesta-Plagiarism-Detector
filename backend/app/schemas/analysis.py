from pydantic import BaseModel
from typing import Any, Dict

class AnalyzeRequest(BaseModel):
    assignment_id: str

class AnalyzeResponse(BaseModel):
    assignment_id: str
    report: Dict[str, Any]
