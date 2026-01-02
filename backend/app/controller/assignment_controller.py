# app/controllers/assignment_controller.py
from fastapi import APIRouter, UploadFile, File
from pathlib import Path

from utils.text_extraction import extract_text
from app.services.analysis.text_similarity import (
    segment_sentences,
    SemanticSimilarityService
)

from app.db.chroma_client import get_chroma_client, ChromaSearchClient
from app.services.scoring.scoring import calculate_score
from app.services.report.report_builder import build_report

router = APIRouter()


@router.post("/upload")
async def upload_assignment(file: UploadFile = File(...)):
    text = extract_text(file)
    sentences = segment_sentences(text)

    return {
        "extracted_text_preview": text[:500],
        "total_sentences": len(sentences),
        "sentences": sentences[:10]
    }


@router.post("/run")
async def run_analysis(assignment_id: str):
    upload_dir = Path(f"data/uploads/{assignment_id}")
    extracted_path = upload_dir / "extracted.txt"

    if not extracted_path.exists():
        return {"error": "Extracted text missing"}

    text = extracted_path.read_text(encoding="utf-8")
    sentences = segment_sentences(text)

    client = get_chroma_client()

    corpus_collection = client.get_collection("corpus_plagiarism")
    print("🔥 DEBUG corpus count:", corpus_collection.count())

    chroma_search = ChromaSearchClient(corpus_collection)

    similarity_service = SemanticSimilarityService(chroma_search)
    semantic_matches = similarity_service.analyze(sentences)

    score = calculate_score(
        total_sentences=len(sentences),
        semantic_matches=semantic_matches
    )

    return build_report(
        assignment_id=assignment_id,
        semantic_matches=semantic_matches,
        score=score
    )
