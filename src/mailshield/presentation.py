def confidence_copy(spam_score: float) -> str:
    if spam_score >= 0.85 or spam_score <= 0.15:
        return "High confidence"
    if spam_score >= 0.65 or spam_score <= 0.35:
        return "Moderate confidence"
    return "Borderline result"

