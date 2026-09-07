"""Tests für die Werte-Begrenzung (clamp)."""

import pytest

from validkit import clamp


def test_value_inside_range_returns_unchanged() -> None:
    assert clamp(5, 0, 10) == 5


def test_value_below_range_clamps_to_low() -> None:
    assert clamp(-3, 0, 10) == 0


def test_value_above_range_clamps_to_high() -> None:
    assert clamp(15, 0, 10) == 10


def test_low_greater_than_high_raises_value_error() -> None:
    with pytest.raises(ValueError):
        clamp(1, 10, 0)


def test_value_equal_to_low_returns_low() -> None:
    assert clamp(0, 0, 10) == 0


def test_value_equal_to_high_returns_high() -> None:
    assert clamp(10, 0, 10) == 10


def test_float_inside_range_returns_unchanged() -> None:
    assert clamp(5.5, 0.0, 10.0) == 5.5


def test_float_below_range_clamps_to_low() -> None:
    assert clamp(-3.5, 0.0, 10.0) == 0.0


def test_float_above_range_clamps_to_high() -> None:
    assert clamp(15.5, 0.0, 10.0) == 10.0


def test_float_low_greater_than_high_raises_value_error() -> None:
    with pytest.raises(ValueError):
        clamp(1.5, 10.0, 0.0)


def test_single_point_interval_returns_low() -> None:
    assert clamp(7, 5, 5) == 5


@pytest.mark.parametrize(
    "value,low,high",
    [
        ("5", 0, 10),
        (None, 0, 10),
        (5, "0", 10),
        (5, 0, "10"),
        ([5], 0, 10),
    ],
)
def test_wrong_type_raises_type_error(value, low, high) -> None:
    with pytest.raises(TypeError):
        clamp(value, low, high)


def test_type_error_message_does_not_contain_input_value() -> None:
    with pytest.raises(TypeError) as excinfo:
        clamp("geheim-wert", 0, 10)
    assert "geheim-wert" not in str(excinfo.value)


def test_value_error_message_does_not_contain_input_value() -> None:
    with pytest.raises(ValueError) as excinfo:
        clamp(1, 10, 0)
    message = str(excinfo.value)
    assert "10" not in message
    assert "0" not in message


def test_error_messages_name_function_and_reason() -> None:
    with pytest.raises(TypeError) as excinfo:
        clamp("x", 0, 10)
    assert "clamp" in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        clamp(1, 10, 0)
    assert "clamp" in str(excinfo.value)


def test_bool_is_int_and_clamps() -> None:
    assert clamp(True, 0, 10) == 1
