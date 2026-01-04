# app/services/analysis/text_similarity.py
from typing import List, Dict, Any
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
EXACT_MATCH_THRESHOLD = 0.90


class SemanticSimilarityService:
    def __init__(self, chroma_client):
        self.chroma = chroma_client
        self.embedder = EmbeddingService()

        count = self.chroma.collection.count()
        if count == 0:
            raise RuntimeError("Corpus collection is EMPTY")

    def analyze(self, sentences: List[str]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []

        for idx, sentence in enumerate(sentences):
            embedding = self.embedder.embed(sentence)
            matches = self.chroma.query(embedding, top_k=3)

            flagged_matches = []

            for doc, meta, dist in zip(
                matches["documents"][0],
                matches["metadatas"][0],
                matches["distances"][0],
            ):
                similarity = 1 - dist

                # only compare against corpus
                if meta.get("type") != "corpus":
                    continue

                if similarity >= SIMILARITY_THRESHOLD:
                    flagged_matches.append({
                        "matched_text": doc,
                        "source": meta.get("source", "Unknown"),
                        "similarity": round(similarity, 3),
                    })

            if not flagged_matches:
                continue

            # sentence-level confidence = best match similarity
            best = max(flagged_matches, key=lambda m: m["similarity"])

            # decide type for scoring
            flag_type = "exact_match" if best["similarity"] >= EXACT_MATCH_THRESHOLD else "semantic"

            results.append({
                "sentence_id": idx,
                "sentence": sentence,
                "type": flag_type,                 
                "confidence": best["similarity"],  
                "source": best["source"],          
                "matches": flagged_matches         
            })
            
            count = self.chroma.collection.count()
        
        if count == 0:
            raise RuntimeError("Corpus collection is EMPTY")

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


