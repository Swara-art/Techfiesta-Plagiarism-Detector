import json
import os
import numpy as np
from functools import lru_cache
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Configuration
# -----------------------------

CORPUS_PATH = os.path.join("data", "offline_corpus.json")
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# -----------------------------
# Lazy-loaded model
# -----------------------------

@lru_cache(maxsize=1)
def get_model():
    print("Loading SentenceTransformer model (offline_corpus)...")
    return SentenceTransformer(MODEL_NAME)

# -----------------------------
# Lazy-loaded corpus
# -----------------------------

@lru_cache(maxsize=1)
def load_corpus():
    """
    Loads corpus only once into memory.
    """
    if not os.path.exists(CORPUS_PATH):
        raise FileNotFoundError(
            f"Offline corpus not found at {CORPUS_PATH}. "
            "Run build_offline_corpus.py first."
        )

    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    texts = [item["text"] for item in corpus]
    sources = [item.get("source", "unknown") for item in corpus]
    embeddings = np.array(
        [item["embedding"] for item in corpus],
        dtype=np.float32
    )

    print(f"Loaded offline corpus with {len(texts)} sentences")
    return texts, sources, embeddings

# -----------------------------
# Core search API
# -----------------------------

def search_offline_corpus(
    query: str,
    top_k: int = 5,
    threshold: float = 0.85
) -> list[dict]:
    """
    Semantic search over offline corpus.

    Args:
        query (str): sentence to search
        top_k (int): max results to return
        threshold (float): similarity cutoff (0–1)

    Returns:
        List of matches with text, source, similarity
    """
    if not query or not query.strip():
        return []

    model = get_model()
    corpus_texts, corpus_sources, corpus_embeddings = load_corpus()

    # Encode query
    query_embedding = model.encode([query])

    # Vectorized cosine similarity
    similarities = cosine_similarity(
        query_embedding,
        corpus_embeddings
    )[0]

    # Get top-K indices (sorted)
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in top_indices:
        score = float(similarities[idx])
        if score < threshold:
            continue

        results.append({
            "text": corpus_texts[idx],
            "source": corpus_sources[idx],
            "similarity": round(score, 4)
        })

    return results
