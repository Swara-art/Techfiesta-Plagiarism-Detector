import nltk
import numpy as np
from functools import lru_cache
from nltk import sent_tokenize
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.offline_corpus import search_offline_corpus
from app.ddg_search import duckduckgo_search

# -----------------------------
# Configuration
# -----------------------------

SIMILARITY_THRESHOLD = 0.85
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


# -----------------------------
# Model + NLP Setup
# -----------------------------

@lru_cache(maxsize=1)
def get_model():
    print("Loading SentenceTransformer model...")
    model = SentenceTransformer(MODEL_NAME)
    print("Model loaded.")
    return model


def ensure_nltk():
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")


# -----------------------------
# Core Semantic Utility
# -----------------------------

def semantic_similarity(source_sentences: list[str], target_sentences: list[str]):
    """
    Compute semantic similarity between two sentence lists.
    Returns list of matches above threshold.
    """
    model = get_model()

    src_emb = model.encode(source_sentences)
    tgt_emb = model.encode(target_sentences)

    sim_matrix = cosine_similarity(src_emb, tgt_emb)

    matches = []
    for i, src_sentence in enumerate(source_sentences):
        best_idx = int(np.argmax(sim_matrix[i]))
        best_score = float(sim_matrix[i][best_idx])

        if best_score >= SIMILARITY_THRESHOLD:
            matches.append({
                "sentence": src_sentence,
                "matched_text": target_sentences[best_idx],
                "similarity": round(best_score, 4)
            })

    return matches


# -----------------------------
# INTERNAL PLAGIARISM
# Offline corpus vs uploaded doc
# -----------------------------

def perform_internal_plagiarism_analysis(text: str) -> dict:
    ensure_nltk()
    sentences = sent_tokenize(text)

    matches = []
    for sentence in sentences:
        corpus_matches = search_offline_corpus(sentence, threshold=SIMILARITY_THRESHOLD)
        if corpus_matches:
            matches.append({
                "sentence": sentence,
                "matches": corpus_matches
            })

    originality = 100.0
    if sentences:
        originality = round(
            (1 - len(matches) / len(sentences)) * 100, 2
        )

    return {
        "type": "internal_plagiarism",
        "overall_originality_score": originality,
        "total_sentences": len(sentences),
        "sentences_flagged": len(matches),
        "matches": matches
    }


# -----------------------------
# EXTERNAL PLAGIARISM
# DuckDuckGo + semantic matching
# -----------------------------

def perform_external_plagiarism_analysis(text: str) -> dict:
    ensure_nltk()
    model = get_model()

    sentences = sent_tokenize(text)
    matches = []

    for sentence in sentences:
        web_snippets = duckduckgo_search(sentence, max_results=5)
        if not web_snippets:
            continue

        sent_emb = model.encode([sentence])
        web_emb = model.encode(web_snippets)

        sims = cosine_similarity(sent_emb, web_emb)[0]

        for idx, score in enumerate(sims):
            if score >= SIMILARITY_THRESHOLD:
                matches.append({
                    "sentence": sentence,
                    "source_text": web_snippets[idx],
                    "similarity": round(float(score), 4)
                })

    originality = 100.0
    if sentences:
        originality = round(
            (1 - len(matches) / len(sentences)) * 100, 2
        )

    return {
        "type": "external_plagiarism",
        "overall_originality_score": originality,
        "total_sentences": len(sentences),
        "matches_found": len(matches),
        "matches": matches
    }


# -----------------------------
# UNIFIED ENTRY (optional helper)
# -----------------------------

def perform_text_plagiarism_analysis(text: str) -> dict:
    """
    Runs both internal and external plagiarism checks.
    """
    internal = perform_internal_plagiarism_analysis(text)
    external = perform_external_plagiarism_analysis(text)

    return {
        "internal_plagiarism": internal,
        "external_plagiarism": external
    }
