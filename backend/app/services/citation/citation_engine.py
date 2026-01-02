from db.chroma_collections import get_collection

def suggest_citations(sentence_embedding):
    collection = get_collection("academic_sources")

    results = collection.query(
        query_embeddings=[sentence_embedding],
        n_results=3
    )

    return results
