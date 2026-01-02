import os
import re
from sentence_transformers import SentenceTransformer
from app.db.chroma_client import get_chroma_client
from dotenv import load_dotenv

load_dotenv()

CORPUS_DIR = "data/corpus"
COLLECTION_NAME = "corpus_plagiarism"

_SENTENCE_SPLIT_REGEX = re.compile(r'(?<=[.!?])\s+')

def split_sentences(text: str):
    return [s.strip() for s in _SENTENCE_SPLIT_REGEX.split(text) if s.strip()]

def ingest_corpus():
    client = get_chroma_client()
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    
    print("Corpus count BEFORE:", collection.count())

    model = SentenceTransformer("all-MiniLM-L6-v2")

    for filename in os.listdir(CORPUS_DIR):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(CORPUS_DIR, filename)
        text = open(path, encoding="utf-8", errors="ignore").read()

        sentences = split_sentences(text)
        if not sentences:
            continue

        embeddings = model.encode(
            sentences,
            normalize_embeddings=True
        ).tolist()

        collection.add(
            ids=[f"{filename}_{i}" for i in range(len(sentences))],
            documents=sentences,
            embeddings=embeddings,
            metadatas=[
                {
                    "source": filename,
                    "type": "corpus"   # 🔐 IMMUTABLE
                }
            ] * len(sentences)
        )

        print(f"✅ Ingested {len(sentences)} sentences from {filename}")
        
    print("Corpus count AFTER:", collection.count())

    print("✅ Corpus ingestion complete")

if __name__ == "__main__":
    ingest_corpus()