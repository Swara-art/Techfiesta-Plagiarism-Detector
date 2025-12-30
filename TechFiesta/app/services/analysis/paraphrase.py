from db.chroma_collections import get_collection

def detect_paraphrase(embedding):
    collection = get_collection("student_text")

    return collection.query(
        query_embeddings=[embedding],
        n_results=3
    )
