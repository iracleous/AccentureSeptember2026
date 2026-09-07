# Tests for ticket score calculation: verifies priority-based scoring with reopen handling

import pytest

from ticket_service import calculate_score


# POSITIVE TEST: Valid low priority should return correct score
def test_calculate_score_low_priority():
    """Test that low priority returns base score of 1"""
    assert calculate_score("low") == 1


# POSITIVE TEST: Valid high priority with reopens should add to base score
def test_calculate_score_with_reopens():
    """Test that reopens add to the base score (high 3 + 2 reopens = 5)"""
    assert calculate_score("high", 2) == 5


# POSITIVE TEST: Unknown priority should safely default to 0
def test_calculate_score_unknown_priority():
    """Test that unknown priority safely returns 0"""
    assert calculate_score("unknown") == 0


# POSITIVE TEST: Unknown priority with reopens should still add reopens
def test_calculate_score_unknown_with_reopens():
    """Test that unknown priority still adds reopens (0 + 2 reopens = 2)"""
    assert calculate_score("unknown", 2) == 2


# POSITIVE TEST: Explicit zero reopens should work correctly
def test_calculate_score_zero_reopens():
    """Test that explicit zero reopens parameter works"""
    assert calculate_score("high", 0) == 3


# NEGATIVE TEST: Negative reopens should raise ValueError
def test_calculate_score_negative_reopens():
    """Test that negative reopens value raises ValueError with correct message"""
    with pytest.raises(ValueError, match="reopens cannot be negative"):
        calculate_score("high", -1)


# NEGATIVE TEST: Invalid reopens type should raise TypeError
def test_calculate_score_invalid_reopens_type():
    """Test that non-integer reopens value raises TypeError"""
    with pytest.raises(TypeError):
        calculate_score("high", "two")
