from typing import List, Dict

def calculate_score(
    total_sentences: int,
    semantic_matches: list[dict]
) -> dict:

    flagged_sentences = len(semantic_matches)

    if total_sentences == 0:
        originality_score = 100.0
    else:
        originality_score = round(
            (1 - (flagged_sentences / total_sentences)) * 100, 2
        )

    plagiarism_score = round(100 - originality_score, 2)

    return {
        "total_sentences": total_sentences,
        "sentences_flagged": flagged_sentences,
        "originality_score": originality_score,
        "plagiarism_score": plagiarism_score,
    }


WEIGHTS = {
    "exact_match": 1.0,
    "paraphrase": 0.7,
    "ai_generated": 0.8
}


def compute_originality_score(
    total_sentences: int,
    flagged_items: List[Dict]
) -> Dict:

    if total_sentences == 0:
        return {
            "originality_score": 100,
            "plagiarism_score": 0,
            "total_sentences": 0,
            "sentences_flagged": 0
        }

    penalty = 0.0
    unique_flagged_sentences = set()

    for item in flagged_items:
        sentence_id = item.get("sentence_id")
        flag_type = item.get("type")

        if sentence_id is None or flag_type not in WEIGHTS:
            continue

        # Prevent double-counting same sentence
        if sentence_id in unique_flagged_sentences:
            continue

        unique_flagged_sentences.add(sentence_id)
        penalty += WEIGHTS[flag_type]

    originality = max(0.0, 1 - (penalty / total_sentences))
    plagiarism = 1 - originality

    return {
        "originality_score": round(originality * 100, 2),
        "plagiarism_score": round(plagiarism * 100, 2),
        "total_sentences": total_sentences,
        "sentences_flagged": len(unique_flagged_sentences)
    }
