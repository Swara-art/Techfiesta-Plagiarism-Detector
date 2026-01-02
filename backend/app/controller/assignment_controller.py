from fastapi import APIRouter, UploadFile, File
from utils.text_extraction import extract_text
from utils.sentence_segmentation import segment_sentences
from pathlib import Path
from app.services.analysis.text_similarity import segment_sentences

router = APIRouter()


@router.post("/assignments/upload")
async def upload_assignment(file: UploadFile = File(...)):
    # Extract text
    text = extract_text(file)
    print("Extracted text length:", len(text))

    # Segment sentences
    sentences = segment_sentences(text)
    print("Segmented sentences:", len(sentences))

    return {
        "extracted_text_preview": text[:500],
        "total_sentences": len(sentences),
        "sentences": sentences[:10]  
    }
    
def debug_assignment(assignment_id: str):
    upload_dir = Path(f"data/uploads/{assignment_id}")
    extracted_path = upload_dir / "extracted.txt"

    if not extracted_path.exists():
        return {"error": "Extracted text missing"}

    text = extracted_path.read_text(encoding="utf-8")
    sentences = segment_sentences(text)

    return {
        "assignment_id": assignment_id,
        "text_length": len(text),
        "sentence_count": len(sentences),
        "sentences": sentences
    }

