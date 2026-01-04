import os
import chromadb
from chromadb.config import Settings

class ChromaSearchClient:
    def __init__(self, collection):
        self.collection = collection

    def query(self, embedding, top_k=3):
        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")
)

CHROMA_PATH = os.path.join(BASE_DIR, "chroma_store")

# Ensure directory exists
os.makedirs(CHROMA_PATH, exist_ok=True)

print("🧠 Using CHROMA_PATH:", CHROMA_PATH)


def get_chroma_client():
    return chromadb.Client(
        Settings(
            is_persistent=True,              
            persist_directory=CHROMA_PATH,
            anonymized_telemetry=False
        )
    )
