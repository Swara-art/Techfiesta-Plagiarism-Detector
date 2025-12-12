import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import json
import nltk
import numpy as np
from tqdm import tqdm
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from app.ddg_search import duckduckgo_search

# -----------------------------
# CONFIG
# -----------------------------

OUTPUT_FILE = "data/offline_corpus.json"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

MAX_WIKI_ARTICLES = 800          # Wikipedia contribution
MAX_DDG_QUERIES = 200            # DuckDuckGo contribution
SIM_THRESHOLD_DEDUP = 0.92       # Remove near-duplicates
MIN_SENT_LEN = 40
MAX_SENT_LEN = 300
MAX_SCAN_ARTICLES = 2000


TOPIC_KEYWORDS = {
    "cs": ["algorithm", "data structure", "compiler", "database", "operating system"],
    "ml": ["machine learning", "neural network", "deep learning", "model", "training"],
    "science": ["physics", "chemistry", "biology", "experiment", "theory"]
}

# -----------------------------
# SETUP
# -----------------------------

nltk.download("punkt")
model = SentenceTransformer(MODEL_NAME)

# -----------------------------
# HELPERS
# -----------------------------

def topic_match(text: str) -> bool:
    text_l = text.lower()
    for keywords in TOPIC_KEYWORDS.values():
        for kw in keywords:
            if kw in text_l:
                return True
    return False


def clean_sentence(s: str) -> str:
    s = s.replace("\n", " ").strip()
    return " ".join(s.split())


def extract_sentences(text: str) -> list[str]:
    sentences = nltk.sent_tokenize(text)

    # Article-level topic match
    if not topic_match(text[:2000]):
        return []

    clean = []
    for s in sentences:
        s = clean_sentence(s)
        if MIN_SENT_LEN <= len(s) <= MAX_SENT_LEN:
            clean.append(s)

    return clean



def deduplicate(sentences: list[str]) -> list[str]:
    if not sentences:
        return []

    embeddings = model.encode(sentences, show_progress_bar=False)
    keep = []
    keep_embs = []

    for sent, emb in zip(sentences, embeddings):
        if not keep_embs:
            keep.append(sent)
            keep_embs.append(emb)
            continue

        sims = cosine_similarity([emb], keep_embs)[0]
        if max(sims) < SIM_THRESHOLD_DEDUP:
            keep.append(sent)
            keep_embs.append(emb)

    return keep


# -----------------------------
# WIKIPEDIA INGESTION
# -----------------------------

def ingest_wikipedia():
    corpus = []
    dataset = load_dataset(
        "wikimedia/wikipedia",
        "20231101.en",
        split="train",
        streaming=True
    )

    count = 0
    scanned = 0

    for item in dataset:
        scanned += 1

        if scanned % 50 == 0:
            print(f"Scanned {scanned} articles, accepted {count}")

        if count >= MAX_WIKI_ARTICLES:
            break
        
        if scanned >= MAX_SCAN_ARTICLES:
            print("Reached scan limit, stopping Wikipedia ingestion")
            break

        text = item["text"]
        sentences = extract_sentences(text)
        if not sentences:
            continue

        sentences = deduplicate(sentences)
        embeddings = model.encode(sentences)

        for s, e in zip(sentences, embeddings):
            corpus.append({
                "text": s,
                "embedding": e.tolist(),
                "source": f"Wikipedia:{item['title']}"
            })

        count += 1

    return corpus


# -----------------------------
# DUCKDUCKGO INGESTION (CACHED)
# -----------------------------

def ingest_duckduckgo():
    corpus = []

    seed_queries = [
        "machine learning basics",
        "operating systems concepts",
        "database indexing",
        "neural networks explanation",
        "physics fundamental laws"
    ]

    for query in seed_queries[:MAX_DDG_QUERIES]:
        snippets = duckduckgo_search(query, max_results=5)

        sentences = []
        for snip in snippets:
            sentences.extend(extract_sentences(snip))

        sentences = deduplicate(sentences)
        embeddings = model.encode(sentences)

        for s, e in zip(sentences, embeddings):
            corpus.append({
                "text": s,
                "embedding": e.tolist(),
                "source": f"DuckDuckGo:{query}"
            })

    return corpus


# -----------------------------
# MAIN
# -----------------------------

def build_corpus():
    print("Ingesting Wikipedia...")
    wiki_corpus = ingest_wikipedia()

    print("Ingesting DuckDuckGo snippets...")
    ddg_corpus = ingest_duckduckgo()

    full_corpus = wiki_corpus + ddg_corpus

    print(f"Final corpus size: {len(full_corpus)} sentences")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(full_corpus, f)

    print(f"Offline corpus saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    build_corpus()
