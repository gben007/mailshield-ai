import re
import string

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from src.mailshield.config import SPAM_TERMS


def clean_text(text: str) -> list[str]:
    normalized = text.lower()
    normalized = re.sub(r"http\S+|www\.\S+", " ", normalized)
    normalized = normalized.translate(str.maketrans("", "", string.punctuation))
    tokens = re.findall(r"\b[a-z]+\b", normalized)
    return [token for token in tokens if token not in ENGLISH_STOP_WORDS]


def extract_signal_terms(tokens: list[str]) -> list[str]:
    return sorted({token for token in tokens if token in SPAM_TERMS})

