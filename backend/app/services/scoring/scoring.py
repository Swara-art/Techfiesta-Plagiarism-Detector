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
