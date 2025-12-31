from fastapi import APIRouter, UploadFile, HTTPException
from pathlib import Path
import uuid
import logging

from app.utils.text_extraction import extract_text_from_file
from app.services.analysis.text_similarity import segment_sentences

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/upload")  # keep your existing response_model as-is
async def upload_assignment(file: UploadFile):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    assignment_id = str(uuid.uuid4())
    upload_dir = Path(f"data/uploads/{assignment_id}")
    upload_dir.mkdir(parents=True, exist_ok=True)

    # 1) Save uploaded file ONCE
    file_path = upload_dir / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 2) Extract text from SAVED file
    extracted_text = extract_text_from_file(file_path)

    # 3) Persist extracted text for later stages
    extracted_path = upload_dir / "extracted.txt"
    extracted_path.write_text(extracted_text, encoding="utf-8")

    # 4) Segment sentences NOW for preview + counts
    sentences = segment_sentences(extracted_text)

    logger.info(f"📁 Saved file at: {file_path}")
    logger.info(f"Extracted text length: {len(extracted_text)}")
    logger.info(f"Segmented sentences: {len(sentences)}")

    # 5) Return fields required by your response_model
    return {
        "assignment_id": assignment_id,
        "filename": file.filename,
        "total_sentences": len(sentences),
        "preview_sentences": sentences[:5],  # small preview for UI/debug
        "status": "uploaded",
    }
