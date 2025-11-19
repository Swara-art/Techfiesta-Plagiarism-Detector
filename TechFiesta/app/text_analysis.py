import nltk
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from functools import lru_cache
from app.web_search import fetch_web_snippets
from nltk import sent_tokenize

SIMILARITY_THRESHOLD = 0.85  # you already had this


# 1. Model loading (lazy, so app startup is lighter)
@lru_cache
def get_model():
    print("Loading semantic similarity model...")
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    print("Model loaded successfully.")
    return model


def ensure_nltk():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab')


def embed_sentences(sentences):
    model = get_model()
    return model.encode(sentences)

def chunk_sentences(sentences, max_chars=350):
    """
    Groups sentences into chunks under the character limit.
    """
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chars:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence  # start new chunk

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def analyze_against_corpus(submission_text: str, corpus: list[str]) -> dict:
    """
    Core engine: compare submission_text against an arbitrary corpus.
    Later, 'corpus' can be:
      - your MOCK_CORPUS
      - web search snippets
      - database docs
    """
    ensure_nltk()

    # 1. Split submission into sentences
    submission_sentences = nltk.sent_tokenize(submission_text)
    if not submission_sentences:
        return {
            "message": "No sentences found to analyze.",
            "matches": [],
            "overall_originality_score": 100,
            "total_sentences": 0,
            "sentences_with_matches": 0,
        }

    # 2. Embed both submission and corpus
    submission_embeddings = embed_sentences(submission_sentences)
    corpus_embeddings = embed_sentences(corpus)

    # 3. Similarity matrix
    sim_matrix = cosine_similarity(submission_embeddings, corpus_embeddings)

    matches = []
    for i, sub_sentence in enumerate(submission_sentences):
        scores_for_sentence = sim_matrix[i]
        best_match_index = int(np.argmax(scores_for_sentence))
        best_score = float(scores_for_sentence[best_match_index])

        if best_score > SIMILARITY_THRESHOLD:
            matches.append({
                "type": "semantic_match",
                "submission_text": sub_sentence,
                "source_text": corpus[best_match_index],
                "similarity": round(best_score, 4),
            })

    original_sentences = len(submission_sentences) - len(matches)
    overall_originality = (original_sentences / len(submission_sentences)) * 100

    return {
        "overall_originality_score": round(overall_originality, 2),
        "total_sentences": len(submission_sentences),
        "sentences_with_matches": len(matches),
        "matches": matches,
    }
    
def perform_web_plagiarism_analysis(submission_text: str) -> dict:
    ensure_nltk()

    sentences = sent_tokenize(submission_text)

    # Create sliding windows
    windows = sliding_windows(sentences, window_size=2, max_chars=250)

    full_matches = []
    matched_windows = 0

    for window in windows:
        web_corpus = fetch_web_snippets(window)

        if not web_corpus:
            continue

        # Compare window against fetched results
        result = analyze_against_corpus(window, web_corpus)

        if result["sentences_with_matches"] > 0:
            matched_windows += 1
            full_matches.extend(result["matches"])

    total_windows = len(windows)
    originality = (
        100 if total_windows == 0 
        else round((1 - matched_windows / total_windows) * 100, 2)
    )

    return {
        "type": "internet_check",
        "overall_originality_score": originality,
        "matches_found": len(full_matches),
        "matches": full_matches,
        "total_windows": total_windows,
        "windows_flagged": matched_windows,
    }


def sliding_windows(sentences, window_size=2, max_chars=250):
    windows = []

    for i in range(len(sentences) - window_size + 1):
        window = " ".join(sentences[i:i+window_size])

        # Hard cap for Tavily
        if len(window) > max_chars:
            window = window[:max_chars]

        windows.append(window)

    return windows



# 4. Backwards-compatible function you already use
MOCK_CORPUS = [
    "The mitochondria is the powerhouse of the cell.",
    "A complicated web of interconnected systems makes up the global economy.",
    "Python is an interpreted, high-level, general-purpose programming language.",
    "Photosynthesis is a process used by plants and other organisms to convert light energy into chemical energy.",
    "The French Revolution was a period of far-reaching social and political upheaval in France."
]


def perform_semantic_analysis(extracted_text: str) -> dict:
    """
    Wrapper that still uses MOCK_CORPUS,
    but internally goes through the generic engine.
    """
    return analyze_against_corpus(extracted_text, MOCK_CORPUS)
