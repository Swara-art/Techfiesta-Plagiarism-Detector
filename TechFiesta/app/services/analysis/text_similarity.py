from typing import List, Dict, Any
from app.db.chroma_client import get_chroma_client
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "plagiarism_corpus"

class TextSimilarityEngine:
    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )
        self.client = get_chroma_client()
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME
        )
        self.threshold = 0.85

    def check_sentences(self, sentences: List[str]) -> List[Dict[str, Any]]:
        if not sentences:
            return []

        embeddings = self.model.encode(sentences).tolist()

        results = self.collection.query(
            query_embeddings=embeddings,
            n_results=1
        )

        matches = []
        for i, distances in enumerate(results["distances"]):
            similarity = 1 - distances[0]  # cosine distance → similarity
            if similarity >= self.threshold:
                matches.append({
                    "sentence_id": i,
                    "score": round(similarity, 3),
                    "matched_text": results["documents"][i][0],
                    "source": results["metadatas"][i][0]["source"]
                })

        return matches
