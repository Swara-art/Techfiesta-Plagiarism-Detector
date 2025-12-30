from fastapi import APIRouter, UploadFile, File
from app.schemas.assignment import AssignmentCreateResponse
from app.services.storage.file_store import FileStore
from app.utils.text_extraction import extract_text_from_bytes
from app.services.preprocessing.segment import segment_sentences

router = APIRouter()
store = FileStore()


@router.post("/upload", response_model=AssignmentCreateResponse)
async def upload_assignment(file: UploadFile = File(...)):
    # 1️⃣ Read file ONCE
    file_bytes = await file.read()

    # 2️⃣ Save file
    await file.seek(0)
    assignment_id = await store.save_upload(file)

    # 3️⃣ Extract text (TXT / PDF / OCR)
    text = extract_text_from_bytes(file.filename, file_bytes)
    print("📝 Extracted text length:", len(text))

    # 4️⃣ Segment sentences
    sentences = segment_sentences(text)
    print("✂️ Segmented sentences:", len(sentences))

    return AssignmentCreateResponse(
        assignment_id=assignment_id,
        filename=file.filename,
        total_sentences=len(sentences),
        preview_sentences=sentences[:5],
    )
