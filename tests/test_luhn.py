"""Tests für die Luhn-Prüfsumme."""

import pytest

from validkit import luhn_check


def test_valid_luhn_number() -> None:
    assert luhn_check("79927398713") is True


def test_changed_digit_is_invalid() -> None:
    assert luhn_check("79927398712") is False


@pytest.mark.parametrize(
    "digits",
    ["0", "18", "018", "4111111111111111"],
)
def test_known_valid_numbers(digits: str) -> None:
    assert luhn_check(digits) is True


@pytest.mark.parametrize(
    "digits",
    ["1", "19", "1234567812345678", "49927398717"],
)
def test_known_invalid_numbers(digits: str) -> None:
    assert luhn_check(digits) is False


def test_leading_zeros_accepted() -> None:
    assert luhn_check("18") is True
    assert luhn_check("018") is True


def test_non_digit_raises_value_error() -> None:
    with pytest.raises(ValueError) as excinfo:
        luhn_check("12a")
    assert "luhn_check" in str(excinfo.value)
    assert "12a" not in str(excinfo.value)


def test_empty_string_raises_value_error() -> None:
    with pytest.raises(ValueError) as excinfo:
        luhn_check("")
    assert "luhn_check" in str(excinfo.value)


@pytest.mark.parametrize("value", [12345, 0, None, ["79927398713"], 12.5])
def test_wrong_type_raises_type_error(value: object) -> None:
    with pytest.raises(TypeError) as excinfo:
        luhn_check(value)  # type: ignore[arg-type]
    assert "luhn_check" in str(excinfo.value)


def test_error_message_never_leaks_input() -> None:
    secret = "79927398713"
    with pytest.raises(ValueError) as excinfo:
        luhn_check(secret + "x")
    message = str(excinfo.value)
    assert secret not in message
    assert "luhn_check" in message
