from db.chroma_collections import get_collection

def detect_ai_content(embedding):
    collection = get_collection("ai_generated")

    return collection.query(
        query_embeddings=[embedding],
        n_results=5
    )
