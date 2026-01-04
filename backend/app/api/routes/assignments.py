from fastapi import APIRouter, UploadFile, HTTPException, File
from pathlib import Path
import uuid
import logging

from app.utils.text_extraction import extract_text_from_file
from app.services.analysis.text_similarity import segment_sentences

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/upload")  # keep your existing response_model as-is
async def upload_assignment(file: UploadFile = File(...)):
    assignment_id = str(uuid.uuid4())
    upload_dir = Path(f"data/uploads/{assignment_id}")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_file(file_path)

    extracted_path = upload_dir / "extracted.txt"
    extracted_path.write_text(text, encoding="utf-8")

    sentences = segment_sentences(text)

    return {
        "assignment_id": assignment_id,
        "filename": file.filename,
        "total_sentences": len(sentences),
<<<<<<< HEAD
        "preview_sentences": sentences[:10],
        "status": "uploaded"
=======
        "preview_sentences": sentences[:5],  # small preview for UI/debug
        "status": "uploaded",
        "message": "File processed successfully",
>>>>>>> c4ebfba30298956cb9105173084d9dbee6ec47b0
    }

