from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings

from app.services.preprocessing.normalize import normalize_and_hash

# Chroma Initialization

def get_chroma_client(persist_dir: str):
    return chromadb.Client(
        Settings(
            persist_directory=persist_dir,
            anonymized_telemetry=False
        )
    )


def get_exact_match_collection(client):
    return client.get_or_create_collection(
        name="exact_sentence_index",
        metadata={"type": "exact_match"}
    )

# Corpus Ingestion

def ingest_corpus_sentences(
    collection,
    sentences: List[str],
    document_id: str
):
    ids, documents, metadatas = [], [], []

    for s in sentences:
        normalized, h = normalize_and_hash(s)
        if not normalized:
            continue

        ids.append(h)
        documents.append(normalized)
        metadatas.append({"document_id": document_id})

    if ids:
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

# Runtime Exact Match


def check_exact_match(
    collection,
    sentences: List[str]
) -> List[Dict[str, Any]]:
    matches = []

    for s in sentences:
        normalized, h = normalize_and_hash(s)
        if not normalized:
            continue

        result = collection.get(ids=[h])

        if result and result.get("ids"):
            matches.append({
                "sentence": s,
                "normalized": normalized,
                "hash": h,
                "confidence": 1.0,
                "type": "exact_match",
                "sources": result["metadatas"]
            })

    return matches
