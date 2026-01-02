# app/db/chroma_collections.py
from app.db.chroma_client import get_chroma_client

COLLECTION_NAMES = {
    "student_text": "student_text",
    "student_code": "student_code",
    "academic_sources": "academic_sources",
    "ai_generated": "ai_generated"
}

def init_chroma_collections():
    client = get_chroma_client()

    for name in COLLECTION_NAMES.values():
        client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )

def get_collection(name: str):
    client = get_chroma_client()
    return client.get_collection(COLLECTION_NAMES[name])
