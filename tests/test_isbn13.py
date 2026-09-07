"""Tests für die ISBN-13-Validierung."""

import pytest

from validkit import is_valid_isbn13


def test_valid_isbn13_with_hyphens() -> None:
    assert is_valid_isbn13("978-3-16-148410-0") is True


def test_valid_isbn13_without_separators() -> None:
    assert is_valid_isbn13("9783161484100") is True


def test_valid_isbn13_with_spaces() -> None:
    assert is_valid_isbn13("978 3 16 148410 0") is True


def test_valid_isbn13_mixed_separators() -> None:
    assert is_valid_isbn13("978 3-16 148410-0") is True


def test_wrong_check_digit_is_false() -> None:
    assert is_valid_isbn13("978-3-16-148410-1") is False


def test_wrong_check_digit_without_separators_is_false() -> None:
    assert is_valid_isbn13("9783161484109") is False


def test_too_short_is_false() -> None:
    assert is_valid_isbn13("978-3-16-148410") is False


def test_too_long_is_false() -> None:
    assert is_valid_isbn13("97831614841000") is False


def test_empty_is_false() -> None:
    assert is_valid_isbn13("") is False


def test_only_separators_is_false() -> None:
    assert is_valid_isbn13("---   ") is False


def test_non_digit_letter_raises_value_error() -> None:
    with pytest.raises(ValueError):
        is_valid_isbn13("978-3-16-14841O-0")


def test_letters_raise_value_error() -> None:
    with pytest.raises(ValueError):
        is_valid_isbn13("abc-def-ghi-jkl-m")


def test_non_string_raises_type_error() -> None:
    with pytest.raises(TypeError):
        is_valid_isbn13(9783161484100)


def test_none_raises_type_error() -> None:
    with pytest.raises(TypeError):
        is_valid_isbn13(None)


def test_over_max_length_returns_false() -> None:
    assert is_valid_isbn13("9" * 10001) is False


def test_over_max_length_with_nondigits_returns_false() -> None:
    assert is_valid_isbn13("a" * 10001) is False


def test_at_max_length_boundary_returns_false() -> None:
    assert is_valid_isbn13("9" * 10000) is False


def test_error_message_names_function_and_reason_only() -> None:
    bad = "978-3-16-14841O-0"
    with pytest.raises(ValueError) as exc:
        is_valid_isbn13(bad)
    message = str(exc.value)
    assert "is_valid_isbn13" in message
    assert bad not in message
