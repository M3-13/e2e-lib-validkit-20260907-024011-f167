"""Tests für die Akzent-Entfernung (strip_accents)."""

import pytest

from validkit import strip_accents


def test_crème_brûlée_becomes_creme_brulee() -> None:
    assert strip_accents("Crème brûlée") == "Creme brulee"


def test_word_without_accents_is_unchanged() -> None:
    assert strip_accents("hello world") == "hello world"


def test_empty_input_returns_empty() -> None:
    assert strip_accents("") == ""


def test_german_umlauts_are_reduced() -> None:
    assert strip_accents("äöü ÄÖÜ") == "aou AOU"


def test_single_accented_letter_is_reduced() -> None:
    assert strip_accents("é") == "e"


def test_non_latin_characters_are_unchanged() -> None:
    assert strip_accents("日本語") == "日本語"


def test_punctuation_and_digits_are_unchanged() -> None:
    assert strip_accents("Höhe 123, mit € und !") == "Hohe 123, mit € und !"


def test_characters_without_decomposition_are_unchanged() -> None:
    assert strip_accents("ßøæ") == "ßøæ"


def test_combining_character_alone_is_removed() -> None:
    assert strip_accents("\u0301") == ""


def test_mixed_accents_and_plain_text() -> None:
    assert strip_accents("Café déjà vu") == "Cafe deja vu"


@pytest.mark.parametrize("value", [None, 123, 3.14, b"bytes", ["e"], {"a": 1}])
def test_wrong_type_raises_type_error(value) -> None:
    with pytest.raises(TypeError):
        strip_accents(value)


def test_type_error_names_function_and_reason() -> None:
    with pytest.raises(TypeError) as excinfo:
        strip_accents(None)
    message = str(excinfo.value)
    assert "strip_accents" in message
    assert "must be a str" in message


def test_type_error_message_does_not_contain_input_value() -> None:
    with pytest.raises(TypeError) as excinfo:
        strip_accents(["geheim-wert"])
    assert "geheim-wert" not in str(excinfo.value)
