import os
import re
from pathlib import Path
from sentence_transformers import SentenceTransformer

from app.db.chroma_client import get_chroma_client
from app.db.chroma_client import CHROMA_PATH
print("🧠 Using CHROMA_PATH:", CHROMA_PATH)

# ==========================
# CONFIG
# ==========================

CORPUS_DIR = Path("data/corpus")
COLLECTION_NAME = "corpus_plagiarism"

SENTENCE_SPLIT_REGEX = re.compile(r'(?<=[.!?])\s+')

# ==========================
# HELPERS
# ==========================

def split_sentences(text: str):
    text = text.replace("\n", " ").strip()
    return [
        s.strip()
        for s in SENTENCE_SPLIT_REGEX.split(text)
        if s.strip() and len(s.strip()) > 10
    ]


# ==========================
# INGESTOR
# ==========================

def ingest_corpus():
    if not CORPUS_DIR.exists():
        raise RuntimeError(f"Corpus directory not found: {CORPUS_DIR}")

    print("📂 Loading corpus from:", CORPUS_DIR.resolve())

    client = get_chroma_client()

    # SAFE: create if missing
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    print("📊 Corpus count BEFORE:", collection.count())

    model = SentenceTransformer("all-MiniLM-L6-v2")

    total_ingested = 0

    for file in CORPUS_DIR.iterdir():
        if not file.name.lower().endswith(".txt"):
            continue

        print(f"📄 Reading {file.name}")

        text = file.read_text(encoding="utf-8", errors="ignore")
        sentences = split_sentences(text)

        if not sentences:
            print(f"⚠️ No sentences found in {file.name}")
            continue

        embeddings = model.encode(
            sentences,
            normalize_embeddings=True,
            show_progress_bar=False
        ).tolist()

        ids = [f"{file.stem}_{i}" for i in range(len(sentences))]

        metadatas = [
            {
                "source": file.name,
                "type": "corpus"
            }
            for _ in sentences
        ]

        collection.add(
            ids=ids,
            documents=sentences,
            embeddings=embeddings,
            metadatas=metadatas
        )
        

        total_ingested += len(sentences)
        print(f"✅ Ingested {len(sentences)} sentences from {file.name}")

    print("📊 Corpus count AFTER:", collection.count())
    print(f"🎉 Total sentences ingested: {total_ingested}")
    # client.persist()
    print("✅ Corpus ingestion complete")
    
    client = get_chroma_client()
    print(client.list_collections())


# ==========================
# ENTRY POINT
# ==========================

if __name__ == "__main__":
    ingest_corpus()
