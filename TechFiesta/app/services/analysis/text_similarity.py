from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from app.db.chroma_collections import get_collection
import re
from typing import List

_SENTENCE_SPLIT_REGEX = re.compile(r'(?<=[.!?])\s+')


def segment_sentences(text: str) -> List[str]:
    if not text:
        return []

    sentences = _SENTENCE_SPLIT_REGEX.split(text)
    return [s.strip() for s in sentences if s.strip()]


class TextSimilarityEngine:
    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )
        self.collection = get_collection("student_text")
        self.threshold = 0.85

    def check_sentences(self, sentences: List[str]) -> List[Dict[str, Any]]:
        if not sentences:
            return []

        embeddings = self.model.encode(sentences, convert_to_numpy=True)

        results = self.collection.query(
            query_embeddings=embeddings.tolist(),
            n_results=1
        )

        matches = []

        for i, distances in enumerate(results["distances"]):
            if not distances:
                continue

            similarity = 1 - distances[0]  # cosine distance → similarity

            if similarity >= self.threshold:
                matches.append({
                    "sentence_id": i,
                    "score": round(similarity, 3),
                    "matched_text": results["documents"][i][0],
                    "source": results["metadatas"][i][0].get("source")
                })

        return matches
