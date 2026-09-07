"""Tests für validkit.phone.normalize_phone."""

import pytest

from validkit.phone import normalize_phone


def test_ac05_german_mobile() -> None:
    assert normalize_phone("0176 12345678", "DE") == "+4917612345678"


def test_already_international_with_plus() -> None:
    assert normalize_phone("+49 176 12345678", "DE") == "+4917612345678"


def test_international_double_zero() -> None:
    assert normalize_phone("0049 176 12345678", "DE") == "+4917612345678"


def test_international_no_trunk() -> None:
    assert normalize_phone("4917612345678", "DE") == "+4917612345678"


def test_separators_hyphen_parentheses_slash() -> None:
    assert normalize_phone("(0176) 123-45678", "DE") == "+4917612345678"
    assert normalize_phone("0176/12345678", "DE") == "+4917612345678"


def test_leading_trailing_whitespace() -> None:
    assert normalize_phone("  0176 12345678  ", "DE") == "+4917612345678"


def test_lowercase_country_code() -> None:
    assert normalize_phone("0176 12345678", "de") == "+4917612345678"


def test_other_country() -> None:
    assert normalize_phone("0664 123456", "AT") == "+43664123456"


def test_unprocessable_letters() -> None:
    with pytest.raises(ValueError):
        normalize_phone("01ab", "DE")


def test_unprocessable_symbols() -> None:
    with pytest.raises(ValueError):
        normalize_phone("!0176", "DE")


def test_empty_input() -> None:
    with pytest.raises(ValueError):
        normalize_phone("", "DE")


def test_only_trunk_zero() -> None:
    with pytest.raises(ValueError):
        normalize_phone("0", "DE")


def test_unsupported_country() -> None:
    with pytest.raises(ValueError):
        normalize_phone("0176 12345678", "XX")


def test_length_over_limit_rejected() -> None:
    with pytest.raises(ValueError):
        normalize_phone("1" * 10001, "DE")


def test_length_at_limit_accepted() -> None:
    result = normalize_phone("1" * 10000, "DE")
    assert result == "+49" + "1" * 10000


def test_non_string_text_type_error() -> None:
    with pytest.raises(TypeError):
        normalize_phone(176, "DE")


def test_non_string_country_type_error() -> None:
    with pytest.raises(TypeError):
        normalize_phone("0176", 49)


def test_error_message_names_function_and_reason_only() -> None:
    with pytest.raises(ValueError) as exc:
        normalize_phone("S3CR3T-PHONE", "DE")
    message = str(exc.value)
    assert "normalize_phone" in message
    assert "S3CR3T" not in message
    assert "PHONE" not in message


def test_error_message_omits_input_value() -> None:
    secret = "069-123456789"
    with pytest.raises(ValueError) as exc:
        normalize_phone(secret, "ZZ")
    assert secret not in str(exc.value)
