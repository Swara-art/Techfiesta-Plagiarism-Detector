import chromadb
from chromadb.config import Settings

CHROMA_PATH = "db/chroma/"

def get_chroma_client():
    return chromadb.Client(
        Settings(
            persist_directory=CHROMA_PATH,
            anonymized_telemetry=False
        )
    )