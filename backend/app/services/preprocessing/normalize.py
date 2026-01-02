import re
import hashlib
from typing import Tuple

_PUNCTUATION_REGEX = re.compile(r"[^\w\s]")
_WHITESPACE_REGEX = re.compile(r"\s+")


def normalize_sentence(sentence: str) -> str:
    if not sentence:
        return ""

    sentence = sentence.lower()
    sentence = _PUNCTUATION_REGEX.sub("", sentence)
    sentence = _WHITESPACE_REGEX.sub(" ", sentence).strip()
    return sentence


def hash_sentence(normalized_sentence: str) -> str:
    if not normalized_sentence:
        return ""
    return hashlib.sha256(normalized_sentence.encode("utf-8")).hexdigest()


def normalize_and_hash(sentence: str) -> Tuple[str, str]:
    normalized = normalize_sentence(sentence)
    return normalized, hash_sentence(normalized)
