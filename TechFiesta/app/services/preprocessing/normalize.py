import re
import hashlib
from typing import Tuple


# Precompiled regex for performance
_PUNCTUATION_REGEX = re.compile(r"[^\w\s]")
_WHITESPACE_REGEX = re.compile(r"\s+")


def normalize_sentence(sentence: str) -> str:
    if not sentence:
        return ""

    # Lowercase
    sentence = sentence.lower()

    # Remove punctuation
    sentence = _PUNCTUATION_REGEX.sub("", sentence)

    # Normalize whitespace
    sentence = _WHITESPACE_REGEX.sub(" ", sentence).strip()

    return sentence


def hash_sentence(normalized_sentence: str) -> str:
    if not normalized_sentence:
        return ""

    return hashlib.sha256(normalized_sentence.encode("utf-8")).hexdigest()


def normalize_and_hash(sentence: str) -> Tuple[str, str]:
    normalized = normalize_sentence(sentence)
    sentence_hash = hash_sentence(normalized)
    return normalized, sentence_hash
