from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings

from app.services.preprocessing.normalize import normalize_and_hash

#Chroma Initialization

def get_chroma_client(persist_dir: str) -> chromadb.Client:
    return chromadb.Client(
        Settings(
            persist_directory=persist_dir,
            anonymized_telemetry=False
        )
    )
    
def get_exact_match_collection(client: chromadb.Client):
    return client.get_or_create_collection(
        name="exact_sentence_index",
        metadata={"purpose": "exact_match_plagiarism"}
    )
    
# Corpus Ingestion (Offline)

def ingest_corpus_sentences(
    collection,
    sentences: List[str],
    document_id: str,
    source: str = "internal"
) -> None:

    ids = []
    documents = []
    metadatas = []

    for sentence in sentences:
        normalized, sentence_hash = normalize_and_hash(sentence)

        if not normalized or not sentence_hash:
            continue

        ids.append(sentence_hash)
        documents.append(normalized)
        metadatas.append({
            "document_id": document_id,
            "source": source
        })

    if ids:
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        
# Runtime Lookup (User Upload)

def check_exact_match(
    collection,
    sentences: List[str]
) -> List[Dict[str, Any]]:
    
    results = []

    for sentence in sentences:
        normalized, sentence_hash = normalize_and_hash(sentence)

        if not normalized or not sentence_hash:
            continue

        lookup = collection.get(ids=[sentence_hash])

        if lookup and lookup.get("ids"):
            results.append({
                "sentence": sentence,
                "normalized_sentence": normalized,
                "sentence_hash": sentence_hash,
                "type": "exact_match",
                "confidence": 1.0,
                "matches": lookup.get("metadatas", [])
            })

    return results