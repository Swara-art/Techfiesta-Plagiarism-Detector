from datetime import datetime

def build_report(
    assignment_id: str,
    semantic_matches: list[dict],
    score: dict
) -> dict:

    return {
        "assignment_id": assignment_id,
        "analysis_type": "semantic_similarity",
        "generated_at": datetime.utcnow().isoformat(),

        "summary": {
            "overall_originality_score": score["originality_score"],
            "plagiarism_score": score["plagiarism_score"],
            "total_sentences": score["total_sentences"],
            "sentences_flagged": score["sentences_flagged"],
        },

        "flagged_items": [
            {
                "sentence": item["sentence"],
                "matches": item["matches"],
            }
            for item in semantic_matches
        ],
    }
