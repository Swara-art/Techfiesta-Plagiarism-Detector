import re
from pathlib import Path
from sentence_transformers import SentenceTransformer

from app.db.chroma_client import get_chroma_client, CHROMA_PATH

print("Using CHROMA_PATH:", CHROMA_PATH)

CORPUS_DIR = Path("data/corpus")
COLLECTION_NAME = "corpus_plagiarism"

SENTENCE_SPLIT_REGEX = re.compile(r'(?<=[.!?])\s+')

def split_sentences(text: str):
    text = text.replace("\n", " ").strip()
    return [
        s.strip()
        for s in SENTENCE_SPLIT_REGEX.split(text)
        if len(s.strip()) > 10
    ]

def ingest_corpus():
    if not CORPUS_DIR.exists():
        raise RuntimeError(f"Corpus directory not found: {CORPUS_DIR.resolve()}")

    print("Loading corpus from:", CORPUS_DIR.resolve())

    client = get_chroma_client()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    print("Corpus count BEFORE:", collection.count())

    model = SentenceTransformer("all-MiniLM-L6-v2")

    total_ingested = 0

    # RECURSIVE INGESTION
    for file in CORPUS_DIR.rglob("*.txt"):
        print(f"Reading {file.relative_to(CORPUS_DIR)}")

        text = file.read_text(encoding="utf-8", errors="ignore")
        sentences = split_sentences(text)

        if not sentences:
            print(f" No sentences found in {file.name}")
            continue

        embeddings = model.encode(
            sentences,
            normalize_embeddings=True,
            show_progress_bar=False
        ).tolist()

        # GLOBAL UNIQUE IDS
        relative_path = file.relative_to(CORPUS_DIR)
        ids = [f"{relative_path}_{i}" for i in range(len(sentences))]

        metadatas = [
            {
                "source": str(relative_path),
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
        print(f"Ingested {len(sentences)} sentences from {file.name}")

    print("Corpus count AFTER:", collection.count())
    print(f"Total sentences ingested this run: {total_ingested}")
    print("Corpus ingestion complete")

    # Debug / sanity check
    print("Available collections:", client.list_collections())


if __name__ == "__main__":
    ingest_corpus()
