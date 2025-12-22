from fastapi import APIRouter, UploadFile, File
from app.schemas.assignment import AssignmentCreateResponse
from app.services.storage.file_store import FileStore

router = APIRouter()
store = FileStore()

@router.post("/upload", response_model=AssignmentCreateResponse)
async def upload_assignment(file: UploadFile = File(...)):
    assignment_id = await store.save_upload(file)
    return AssignmentCreateResponse(
        assignment_id=assignment_id,
        filename=file.filename
    )
