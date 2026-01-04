from app.db.chroma_collections import get_collection
from typing import List, Dict
from sentence_transformers import SentenceTransformer, util

PARAPHRASE_THRESHOLD = 0.75
SEMANTIC_UPPER_BOUND = 0.85
TOP_K = 5

def detect_paraphrase(embedding):
    collection = get_collection("corpus_plagiarism")

    return collection.query(
        query_embeddings=[embedding],
        n_results=3
    )

class ParaphraseDetector:

    def __init__(self):
        self.model = SentenceTransformer("paraphrase-mpnet-base-v2")

    def detect(
        self,
        sentence_id: int,
        sentence: str,
        corpus_sentences: List[str]
    ) -> List[Dict]:

        if not sentence.strip() or not corpus_sentences:
            return []

        # Encode query & corpus
        query_embedding = self.model.encode(sentence, convert_to_tensor=True)
        corpus_embeddings = self.model.encode(corpus_sentences, convert_to_tensor=True)

        # Compute cosine similarity
        similarities = util.cos_sim(query_embedding, corpus_embeddings)[0]

        results = []

        for idx, score in enumerate(similarities):
            confidence = float(score)

            # Paraphrase band
            if PARAPHRASE_THRESHOLD <= confidence < SEMANTIC_UPPER_BOUND:
                results.append({
                    "sentence_id": sentence_id,
                    "type": "paraphrase",
                    "confidence": round(confidence, 3),
                    "matched_sentence": corpus_sentences[idx]
                })

            if len(results) >= TOP_K:
                break

        return results