from db.chroma_collections import get_collection

def check_code_similarity(code_embedding):
    collection = get_collection("student_code")

    return collection.query(
        query_embeddings=[code_embedding],
        n_results=5
    )
