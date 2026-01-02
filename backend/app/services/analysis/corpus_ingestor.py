import os
from sentence_transformers import SentenceTransformer
from app.db.chroma_client import get_chroma_client

CORPUS_DIR = "data/corpus"
COLLECTION_NAME = "plagiarism_corpus"

def ingest_corpus():
    client = get_chroma_client()
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    total_sentences = 0

    for filename in os.listdir(CORPUS_DIR):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(CORPUS_DIR, filename)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read().strip()

        if not text:
            print(f"⚠️ Skipping empty file: {filename}")
            continue

        # safer sentence split
        raw_sentences = text.replace("\n", " ").split(".")
        sentences = [s.strip() for s in raw_sentences if s.strip()]

        if not sentences:
            print(f"⚠️ No valid sentences in: {filename}")
            continue

        embeddings = model.encode(sentences).tolist()

        ids = [f"{filename}_{i}" for i in range(len(sentences))]
        metadatas = [{"source": filename} for _ in sentences]

        collection.add(
            documents=sentences,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )

        total_sentences += len(sentences)
        print(f"Ingested {len(sentences)} sentences from {filename}")

    print(f"\nCorpus ingestion complete. Total sentences: {total_sentences}")
