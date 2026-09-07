"""Tests für die Slug-Erzeugung."""

import pytest

from validkit import slugify


def test_ac08_hello_world() -> None:
    assert slugify("Héllo Wörld!") == "hello-world"


def test_lowercase() -> None:
    assert slugify("HELLO World") == "hello-world"


def test_umlaute() -> None:
    assert slugify("Übermäßig ätzend") == "ubermassig-atzend"


def test_special_characters() -> None:
    assert slugify("Hello, World! How are you?") == "hello-world-how-are-you"


def test_multiple_hyphens_collapse() -> None:
    assert slugify("hello   world") == "hello-world"


def test_leading_and_trailing_hyphens_removed() -> None:
    assert slugify("---hello-world---") == "hello-world"


def test_digits_are_kept() -> None:
    assert slugify("Version 2.0") == "version-2-0"


def test_only_special_characters() -> None:
    assert slugify("!!!###$$$") == ""


def test_empty_string() -> None:
    assert slugify("") == ""


def test_max_length_allowed() -> None:
    assert slugify("a" * 10_000) == "a" * 10_000


def test_over_max_length_rejected() -> None:
    with pytest.raises(ValueError):
        slugify("a" * 10_001)


def test_over_max_length_error_message() -> None:
    with pytest.raises(ValueError) as excinfo:
        slugify("a" * 10_001)
    message = str(excinfo.value)
    assert "slugify" in message
    assert "10" not in message or "maximal" in message


def test_wrong_type_raises_type_error() -> None:
    with pytest.raises(TypeError):
        slugify(123)  # type: ignore[arg-type]


def test_error_message_does_not_contain_input() -> None:
    secret = "geheime-eingabe-123"
    with pytest.raises(ValueError) as excinfo:
        slugify(secret + "a" * 10_001)
    assert secret not in str(excinfo.value)
