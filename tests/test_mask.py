"""Tests für die Maskierung von Geheimnissen."""

import pytest

from validkit import mask_secret


def test_masks_all_but_last_keep() -> None:
    assert mask_secret("geheim123", 4) == "*****m123"


def test_only_last_keep_chars_stay_unchanged() -> None:
    result = mask_secret("geheim123", 4)
    assert result == "*****" + "m123"
    assert result.endswith("m123")
    assert result[:-4] == "*" * (len(result) - 4)


def test_default_keep_is_four() -> None:
    assert mask_secret("geheim123") == "*****m123"


def test_keep_equal_to_length_returns_text_unchanged() -> None:
    assert mask_secret("abc", 3) == "abc"


def test_keep_zero_masks_everything() -> None:
    assert mask_secret("geheim123", 0) == "*********"


def test_empty_text_with_keep_zero() -> None:
    assert mask_secret("", 0) == ""


def test_keep_greater_than_length_raises_value_error() -> None:
    with pytest.raises(ValueError):
        mask_secret("abc", 5)


def test_negative_keep_raises_value_error() -> None:
    with pytest.raises(ValueError):
        mask_secret("abc", -1)


def test_non_string_text_raises_type_error() -> None:
    with pytest.raises(TypeError):
        mask_secret(123, 4)  # type: ignore[arg-type]


def test_non_int_keep_raises_type_error() -> None:
    with pytest.raises(TypeError):
        mask_secret("abc", 2.0)  # type: ignore[arg-type]


def test_error_messages_contain_function_name_and_reason() -> None:
    with pytest.raises(ValueError) as exc_info:
        mask_secret("abc", 5)
    message = str(exc_info.value)
    assert "mask_secret" in message
    assert "abc" not in message


def test_error_messages_do_not_leak_input() -> None:
    with pytest.raises(TypeError) as exc_info:
        mask_secret("topsecret", "4")  # type: ignore[arg-type]
    assert "topsecret" not in str(exc_info.value)
