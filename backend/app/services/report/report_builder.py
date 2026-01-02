from typing import List, Dict, Any

def build_report(sentences: List[str], matches: List[Dict[str, Any]]) -> Dict[str, Any]:
    flagged = {m["sentence_id"]: m for m in matches}

    items = []
    for idx, s in enumerate(sentences):
        if idx in flagged:
            m = flagged[idx]
            items.append({
                "sentence_id": idx,
                "text": s,
                "flagged": True,
                "reason": "high_semantic_similarity",
                "similarity": m["score"],
                "matched_source": m["source"],
                "matched_text": m["matched_source_text"],
                "citation_required": True
            })
        else:
            items.append({
                "sentence_id": idx,
                "text": s,
                "flagged": False
            })

    total = len(sentences) if sentences else 1
    flagged_count = len(matches)
    originality = round(100.0 * (1 - (flagged_count / total)), 2)

    return {
        "overall_originality_score": originality,
        "total_sentences": len(sentences),
        "sentences_flagged": flagged_count,
        "items": items
    }
