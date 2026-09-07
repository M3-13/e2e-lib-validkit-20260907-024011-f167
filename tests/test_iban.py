"""Tests für die IBAN-Validierung (Modulo-97)."""

import pytest

from validkit import is_valid_iban


def test_valid_german_iban() -> None:
    assert is_valid_iban("DE89 3704 0044 0532 0130 00") is True


def test_valid_german_iban_without_spaces() -> None:
    assert is_valid_iban("DE89370400440532013000") is True


def test_valid_iban_lowercase() -> None:
    assert is_valid_iban("de89 3704 0044 0532 0130 00") is True


def test_valid_iban_with_hyphens() -> None:
    assert is_valid_iban("DE89-3704-0044-0532-0130-00") is True


@pytest.mark.parametrize(
    "iban",
    [
        "GB29 NWBK 6016 1331 9268 19",
        "FR14 2004 1010 0505 0001 3M02 606",
        "NL91 ABNA 0417 1643 00",
    ],
)
def test_known_valid_ibans_from_other_countries(iban: str) -> None:
    assert is_valid_iban(iban) is True


def test_changed_check_digit_is_invalid() -> None:
    assert is_valid_iban("DE89 3704 0044 0532 0130 01") is False


def test_changed_account_part_is_invalid() -> None:
    assert is_valid_iban("DE89 3704 0044 0532 0131 00") is False


def test_changed_country_code_is_invalid() -> None:
    assert is_valid_iban("DE88 3704 0044 0532 0130 00") is False


def test_too_short_iban_is_invalid() -> None:
    assert is_valid_iban("DE890000") is False


def test_too_long_iban_is_invalid() -> None:
    assert is_valid_iban("DE89" + "0" * 31) is False


def test_iban_not_starting_with_letters_is_invalid() -> None:
    assert is_valid_iban("123456789012345") is False


def test_input_over_limit_rejected_immediately() -> None:
    assert is_valid_iban("A" * 10001) is False


def test_input_at_limit_not_rejected_by_guard() -> None:
    assert is_valid_iban("A" * 10000) is False


def test_empty_string_raises_value_error() -> None:
    with pytest.raises(ValueError) as excinfo:
        is_valid_iban("")
    assert "is_valid_iban" in str(excinfo.value)


def test_invalid_character_raises_value_error() -> None:
    with pytest.raises(ValueError) as excinfo:
        is_valid_iban("DE89!3704 0044 0532 0130 00")
    assert "is_valid_iban" in str(excinfo.value)
    assert "DE89!3704" not in str(excinfo.value)


def test_non_ascii_character_raises_value_error() -> None:
    with pytest.raises(ValueError):
        is_valid_iban("DE89 3704 0044 0532 0130 é0")


@pytest.mark.parametrize("value", [12345, 0, None, ["DE89370400440532013000"], 12.5])
def test_wrong_type_raises_type_error(value: object) -> None:
    with pytest.raises(TypeError) as excinfo:
        is_valid_iban(value)  # type: ignore[arg-type]
    assert "is_valid_iban" in str(excinfo.value)


def test_error_message_never_leaks_input() -> None:
    secret = "DE89 3704 0044 0532 0130 00"
    with pytest.raises(ValueError) as excinfo:
        is_valid_iban(secret + "!")
    message = str(excinfo.value)
    assert secret not in message
    assert "is_valid_iban" in message
