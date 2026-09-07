"""Prüfe, dass alle neun öffentlichen Namen importierbar sind und die
erwarteten Signaturen besitzen."""

import inspect

import validkit


def test_all_nine_names_importable() -> None:
    expected = {
        "is_valid_email",
        "luhn_check",
        "is_valid_iban",
        "is_valid_isbn13",
        "normalize_phone",
        "strip_accents",
        "mask_secret",
        "slugify",
        "clamp",
    }
    assert expected <= set(validkit.__all__)
    for name in expected:
        assert hasattr(validkit, name)


def test_public_signatures() -> None:
    expected = {
        "is_valid_email": ["text"],
        "luhn_check": ["digits"],
        "is_valid_iban": ["text"],
        "is_valid_isbn13": ["text"],
        "normalize_phone": ["text", "country_code"],
        "strip_accents": ["text"],
        "mask_secret": ["text", "keep"],
        "slugify": ["text"],
        "clamp": ["value", "low", "high"],
    }
    for name, params in expected.items():
        func = getattr(validkit, name)
        sig = inspect.signature(func)
        assert list(sig.parameters) == params
        assert callable(func)


def test_mask_secret_keep_default() -> None:
    sig = inspect.signature(validkit.mask_secret)
    assert sig.parameters["keep"].default == 4
