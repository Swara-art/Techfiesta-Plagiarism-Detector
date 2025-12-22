from fastapi import APIRouter, HTTPException
from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.services.storage.file_store import FileStore
from app.services.preprocessing.extract_text import extract_text_from_assignment
from app.services.preprocessing.segment import segment_sentences
from app.services.analysis.text_similarity import TextSimilarityEngine
from app.services.report.report_builder import build_report

router = APIRouter()
store = FileStore()
sim_engine = TextSimilarityEngine()

@router.post("/run", response_model=AnalyzeResponse)
def run_analysis(payload: AnalyzeRequest):
    assignment_dir = store.get_assignment_dir(payload.assignment_id)
    if not assignment_dir:
        raise HTTPException(status_code=404, detail="Assignment not found")

    text = extract_text_from_assignment(assignment_dir)
    print("📝 Extracted text:", repr(text))

    sentences = segment_sentences(text)
    print("✂️ Segmented sentences:", sentences)


    # core semantic check
    matches = sim_engine.check_sentences(sentences)

    report = build_report(sentences=sentences, matches=matches)
    return AnalyzeResponse(assignment_id=payload.assignment_id, report=report)
