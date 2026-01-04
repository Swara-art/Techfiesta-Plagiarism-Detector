# app/services/analysis/text_similarity.py
from typing import List
from sentence_transformers import SentenceTransformer
import re
from app.services.analysis.paraphrase import ParaphraseDetector

_SENTENCE_SPLIT_REGEX = re.compile(r'(?<=[.!?])\s+')

def segment_sentences(text: str) -> List[str]:
    return [s.strip() for s in _SENTENCE_SPLIT_REGEX.split(text) if s.strip()]


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, sentence: str) -> list[float]:
        return self.model.encode(
            sentence,
            normalize_embeddings=True
        ).tolist()


SIMILARITY_THRESHOLD = 0.72 


class SemanticSimilarityService:
    def __init__(self, chroma_client):
        self.chroma = chroma_client
        self.embedder = EmbeddingService()

        count = self.chroma.collection.count()
        if count == 0:
            raise RuntimeError("Corpus collection is EMPTY")

    def analyze(self, sentences: list[str]):
        results = []

        for sentence in sentences:
            embedding = self.embedder.embed(sentence)

            matches = self.chroma.query(embedding, top_k=3)

            flagged = []

            for doc, meta, dist in zip(
                matches["documents"][0],
                matches["metadatas"][0],
                matches["distances"][0],
            ):
                similarity = 1 - dist

                if meta.get("type") != "corpus":
                    continue

                if similarity >= SIMILARITY_THRESHOLD:
                    flagged.append({
                        "matched_text": doc,
                        "source": meta["source"],
                        "similarity": round(similarity, 3),
                    })

            if flagged:
                results.append({
                    "sentence": sentence,
                    "matches": flagged
                })

        return results
    
paraphrase_detector = ParaphraseDetector()

def run_paraphrase_analysis(sentences, corpus_sentences):
    paraphrase_results = []

    for idx, sentence in enumerate(sentences):
        matches = paraphrase_detector.detect(
            sentence_id=idx,
            sentence=sentence,
            corpus_sentences=corpus_sentences
        )
        paraphrase_results.extend(matches)

    return paraphrase_results
