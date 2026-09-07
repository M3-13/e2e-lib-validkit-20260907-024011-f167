"""Werte-Begrenzung."""

from typing import TypeVar

T = TypeVar("T", int, float)


def clamp(value: T, low: T, high: T) -> T:  # noqa: UP047
    # TypeVar stays: the library supports Python 3.11 (PEP 695 needs 3.12).
    """Begrenze *value* auf das Intervall [*low*, *high*]."""
    if not isinstance(value, (int, float)):
        raise TypeError("clamp: value must be an int or float")
    if not isinstance(low, (int, float)):
        raise TypeError("clamp: low must be an int or float")
    if not isinstance(high, (int, float)):
        raise TypeError("clamp: high must be an int or float")
    if low > high:
        raise ValueError("clamp: low must not be greater than high")
    if value < low:
        return low
    if value > high:
        return high
    return value
