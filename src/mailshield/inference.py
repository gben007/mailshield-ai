from __future__ import annotations

import pickle
from dataclasses import dataclass
from pathlib import Path

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

from src.mailshield.preprocessing import clean_text, extract_signal_terms


@dataclass(frozen=True)
class ArtifactBundle:
    model: object
    tokenizer: object
    config: dict
    label_mapping: dict


@dataclass(frozen=True)
class PredictionResult:
    label: str
    spam_score: float
    ham_score: float
    tokens: list[str]
    signal_terms: list[str]


def load_artifacts(artifact_dir: Path) -> ArtifactBundle:
    base = artifact_dir.expanduser().resolve()
    required_files = {
        "model": base / "gru_model.keras",
        "tokenizer": base / "tokenizer.pkl",
        "config": base / "config.pkl",
        "label_mapping": base / "label_mapping.pkl",
    }

    missing = [name for name, path in required_files.items() if not path.exists()]
    if missing:
        missing_items = ", ".join(missing)
        raise FileNotFoundError(f"Missing required artifact files: {missing_items}")

    model = load_model(required_files["model"])
    with required_files["tokenizer"].open("rb") as file:
        tokenizer = pickle.load(file)
    with required_files["config"].open("rb") as file:
        config = pickle.load(file)
    with required_files["label_mapping"].open("rb") as file:
        label_mapping = pickle.load(file)

    return ArtifactBundle(
        model=model,
        tokenizer=tokenizer,
        config=config,
        label_mapping=label_mapping,
    )


def predict_message(text: str, artifact_dir: Path) -> PredictionResult:
    artifacts = load_artifacts(artifact_dir)
    tokens = clean_text(text)
    sequence = artifacts.tokenizer.texts_to_sequences([tokens])
    padded = pad_sequences(sequence, maxlen=artifacts.config["max_length"], padding="post")
    spam_score = float(artifacts.model.predict(padded, verbose=0)[0][0])
    predicted_index = int(spam_score >= 0.5)
    label = artifacts.label_mapping.get(predicted_index, "Spam" if predicted_index else "Ham")

    return PredictionResult(
        label=label,
        spam_score=spam_score,
        ham_score=1 - spam_score,
        tokens=tokens,
        signal_terms=extract_signal_terms(tokens),
    )
