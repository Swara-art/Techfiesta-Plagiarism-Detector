import chromadb
from chromadb.config import Settings

client = chromadb.Client(
    Settings(
        persist_directory="./chroma_store",
        anonymized_telemetry=False
    )
)

col = client.get_or_create_collection("test")

col.add(
    ids=["1"],
    documents=["Machine learning is fun"],
    metadatas=[{"type": "corpus"}]
)

res = col.query(
    query_texts=["What is machine learning?"],
    n_results=1
)

print(res)
