from fastapi import APIRouter, HTTPException
from pathlib import Path
import logging

from app.db.chroma_client import get_chroma_client
from app.services.plagiarism.exact_match import (
    get_exact_match_collection,
    check_exact_match
)
from app.services.analysis.text_similarity import segment_sentences

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/run")
def run_analysis(assignment_id: str):
    upload_dir = Path(f"data/uploads/{assignment_id}")
    extracted_path = upload_dir / "extracted.txt"

    if not extracted_path.exists():
        raise HTTPException(status_code=400, detail="Extracted text not found")

    # 1️⃣ Load extracted text
    text = extracted_path.read_text(encoding="utf-8")

    # 2️⃣ Sentence segmentation
    sentences = segment_sentences(text)
    total_sentences = len(sentences)

    logger.info(f"Segmented sentences: {total_sentences}")

    # 3️⃣ Stage 3: Exact Match
    client = get_chroma_client()
    collection = get_exact_match_collection(client)

    exact_matches = check_exact_match(collection, sentences)

    # 4️⃣ Build REQUIRED report object
    report = {
        "overall_originality_score": (
            100 if total_sentences == 0
            else round(
                100 * (1 - len(exact_matches) / total_sentences),
                2
            )
        ),
        "total_sentences": total_sentences,
        "sentences_flagged": len(exact_matches),
        "items": exact_matches
    }

    # 5️⃣ RETURN WHAT THE RESPONSE MODEL EXPECTS
    return {
        "assignment_id": assignment_id,
        "report": report
    }
