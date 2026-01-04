from datetime import datetime
from typing import List, Dict


def build_report(
    assignment_id: str,
    sentences: List[str],
    flagged_items: List[Dict],
    score: Dict
) -> Dict:

    report_items = []

    for item in flagged_items:
        sentence_id = item.get("sentence_id")

        # Safety checks
        if sentence_id is None or sentence_id >= len(sentences):
            continue

        report_items.append({
            "sentence": sentences[sentence_id],
            "type": item.get("type"),
            "confidence": item.get("confidence"),
            "source": item.get("source", "Unknown")
        })

    return {
        "assignment_id": assignment_id,
        "generated_at": datetime.utcnow().isoformat(),

        "overall_originality_score": score["originality_score"],
        "plagiarism_score": score["plagiarism_score"],
        "total_sentences": score["total_sentences"],
        "sentences_flagged": score["sentences_flagged"],

        "items": report_items
    }