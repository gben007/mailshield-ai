from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ARTIFACT_DIR = PROJECT_ROOT

MODEL_SPECS = {
    "family": "GRU",
    "max_length": 500,
    "max_features": 5000,
}

SPAM_TERMS = {
    "winner",
    "won",
    "urgent",
    "claim",
    "free",
    "cash",
    "offer",
    "limited",
    "click",
    "prize",
    "bonus",
    "guaranteed",
}

SAMPLE_EMAILS = {
    "Promotional spam": (
        "Congratulations. You have won a free cash prize. Click the link now to claim your reward."
    ),
    "Normal work email": (
        "Hi team, the client review is moved to 3 PM tomorrow. Please share your updated slides before lunch."
    ),
    "Urgent finance bait": (
        "Urgent action required. Your account will be suspended unless you confirm payment details immediately."
    ),
}

