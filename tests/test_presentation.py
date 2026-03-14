from src.mailshield.presentation import confidence_copy


def test_confidence_copy_for_high_confidence():
    assert confidence_copy(0.91) == "High confidence"
    assert confidence_copy(0.08) == "High confidence"


def test_confidence_copy_for_moderate_confidence():
    assert confidence_copy(0.72) == "Moderate confidence"
    assert confidence_copy(0.30) == "Moderate confidence"


def test_confidence_copy_for_borderline():
    assert confidence_copy(0.50) == "Borderline result"
