# app/db/chroma_client.py
import chromadb
from chromadb.config import Settings
import os

# 🔥 ABSOLUTE PROJECT ROOT
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")
)

CHROMA_PATH = os.path.join(BASE_DIR, "chroma_store")

_CLIENT = None

def get_chroma_client():
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = chromadb.Client(
            Settings(
                persist_directory=CHROMA_PATH,
                anonymized_telemetry=False
            )
        )
    return _CLIENT


class ChromaSearchClient:
    def __init__(self, collection):
        self.collection = collection

    def query(self, embedding: list[float], top_k: int = 5):
        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
