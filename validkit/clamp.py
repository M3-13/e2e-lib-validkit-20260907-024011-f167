"""Werte-Begrenzung."""

from typing import TypeVar

T = TypeVar("T", int, float)


def clamp(value: T, low: T, high: T) -> T:  # noqa: UP047
    # TypeVar stays: the library supports Python 3.11 (PEP 695 needs 3.12).
    """Begrenze *value* auf das Intervall [*low*, *high*]."""
    raise NotImplementedError
