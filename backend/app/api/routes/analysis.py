from fastapi import APIRouter, HTTPException
from pathlib import Path
import logging

from app.db.chroma_client import get_chroma_client, ChromaSearchClient

from app.services.analysis.text_similarity import segment_sentences
from app.services.analysis.text_similarity import SemanticSimilarityService
from app.services.analysis.paraphrase import ParaphraseDetector
from app.services.scoring.scoring import compute_originality_score
from app.services.report.report_builder import build_report

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/run")
def run_analysis(assignment_id: str):
    upload_dir = Path(f"data/uploads/{assignment_id}")
    extracted_path = upload_dir / "extracted.txt"

    if not extracted_path.exists():
        raise HTTPException(status_code=400, detail="Extracted text not found")

    # Load text
    text = extracted_path.read_text(encoding="utf-8")
    sentences = segment_sentences(text)

    # Chroma
    client = get_chroma_client()
    corpus_collection = client.get_or_create_collection(
        name="corpus_plagiarism",
        metadata={"hnsw:space": "cosine"}
    )
    chroma_search = ChromaSearchClient(corpus_collection)

    # Semantic similarity
    similarity_service = SemanticSimilarityService(chroma_search)
    semantic_matches = similarity_service.analyze(sentences)

    # Paraphrase detection
    paraphrase_detector = ParaphraseDetector()
    paraphrase_matches = []

    for i, s in enumerate(sentences):
        paraphrase_matches.extend(
            paraphrase_detector.detect(
                sentence_id=i,
                sentence=s,
                corpus_sentences=corpus_collection.get()["documents"]
            )
        )

    # Merge flags
    flagged_items = semantic_matches + paraphrase_matches

    # Scoring
    score = compute_originality_score(
        total_sentences=len(sentences),
        flagged_items=flagged_items
    )

    # Final report
    report = build_report(
        assignment_id=assignment_id,
        sentences=sentences,
        flagged_items=flagged_items,
        score=score
    )
    
    print("Corpus count:", corpus_collection.count())

    return {
        "assignment_id": assignment_id,
        "report": report
    }
