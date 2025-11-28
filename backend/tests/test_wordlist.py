"""Tests for word list management."""
import pytest
from word_manager.word_manager import wordlist


def test_wordlist_loading():
    """Test that wordlist loads correctly."""
    words = wordlist.words
    assert len(words) > 0, "Word list is empty"
    assert len(words) > 1000, "Word list suspiciously small"


def test_wordlist_word_length():
    """Test that all words are 5 letters."""
    words = wordlist.words
    invalid_words = [w for w in words if len(w) != 5]
    assert len(invalid_words) == 0, f"Found {len(invalid_words)} words not 5 letters"


def test_wordlist_uppercase():
    """Test that all words are uppercase."""
    words = wordlist.words
    lowercase_words = [w for w in words if not w.isupper()]
    assert len(lowercase_words) == 0, f"Found {len(lowercase_words)} lowercase words"


def test_valid_word():
    """Test validation of valid words."""
    assert wordlist.is_valid("ALEPH"), "Failed to validate ALEPH"
    assert wordlist.is_valid("ZEROS"), "Failed to validate ZEROS"


def test_invalid_word():
    """Test rejection of invalid words."""
    assert not wordlist.is_valid("ZZZZZ"), "Accepted invalid word ZZZZZ"
    assert not wordlist.is_valid("XXXXX"), "Accepted invalid word XXXXX"


def test_word_length_validation():
    """Test that words of wrong length are rejected."""
    assert not wordlist.is_valid("ABC"), "Accepted 3-letter word"
    assert not wordlist.is_valid("ABCDEF"), "Accepted 6-letter word"
    assert not wordlist.is_valid(""), "Accepted empty string"


def test_case_insensitive_validation():
    """Test that validation is case-insensitive."""
    assert wordlist.is_valid("aleph"), "Failed lowercase validation"
    assert wordlist.is_valid("AlEpH"), "Failed mixed-case validation"