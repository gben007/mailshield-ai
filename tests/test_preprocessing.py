from src.mailshield.preprocessing import clean_text, extract_signal_terms


def test_clean_text_removes_links_punctuation_and_stopwords():
    text = "Hi team! Click https://example.com to claim your FREE cash reward now."

    tokens = clean_text(text)

    assert "https" not in tokens
    assert "team" in tokens
    assert "click" in tokens
    assert "free" in tokens
    assert "to" not in tokens


def test_extract_signal_terms_returns_unique_sorted_matches():
    tokens = ["urgent", "offer", "hello", "offer"]

    signal_terms = extract_signal_terms(tokens)

    assert signal_terms == ["offer", "urgent"]

