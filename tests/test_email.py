"""Tests für validkit.email.is_valid_email."""

import ast
import inspect

import pytest

from validkit import email as email_module
from validkit.email import is_valid_email


@pytest.mark.parametrize(
    "address",
    [
        "user@example.com",
        "first.last@sub.example.org",
        "a@b.co",
        "user+tag@example.com",
        "USER@EXAMPLE.COM",
        "1@2.3",
    ],
)
def test_valid_emails(address: str) -> None:
    assert is_valid_email(address) is True


@pytest.mark.parametrize(
    "address",
    [
        "",
        " ",
        "nicht@",
        "a@b",
        "@example.com",
        "user@",
        "user@example",
        "user@.com",
        "user@example.",
    ],
)
def test_invalid_emails(address: str) -> None:
    assert is_valid_email(address) is False


def test_ac01_cases() -> None:
    assert is_valid_email("user@example.com") is True
    assert is_valid_email("nicht@") is False
    assert is_valid_email("a@b") is False


def test_multiple_at_rejected() -> None:
    assert is_valid_email("a@b@c.com") is False
    assert is_valid_email("a@@b.com") is False
    assert is_valid_email("@a@b.com") is False


def test_missing_dot_rejected() -> None:
    assert is_valid_email("user@localhost") is False
    assert is_valid_email("a@b") is False


def test_length_upper_bound_rejected_immediately() -> None:
    # Über der Obergrenze — selbst eine ansonsten gültige Adresse -> False.
    too_long = "a" * 10000 + "@b.c"
    assert len(too_long) == 10004
    assert is_valid_email(too_long) is False


def test_length_at_boundary_is_processed() -> None:
    # Genau 10.000 Zeichen ist keine Überschreitung und wird geprüft.
    at_limit = "a" * 9996 + "@b.c"
    assert len(at_limit) == 10000
    assert is_valid_email(at_limit) is True


def test_wrong_type_raises_typeerror() -> None:
    for bad in (None, 42, 1.5, ["user@example.com"], {"user@example.com"}, b"user@example.com"):
        with pytest.raises(TypeError) as excinfo:
            is_valid_email(bad)  # type: ignore[arg-type]
        message = str(excinfo.value)
        assert "is_valid_email" in message
        assert repr(bad) not in message


def test_error_message_names_reason_without_input_value() -> None:
    with pytest.raises(TypeError) as excinfo:
        is_valid_email(12345)  # type: ignore[arg-type]
    message = str(excinfo.value)
    assert "is_valid_email" in message
    assert "12345" not in message


def test_no_forbidden_dynamic_execution() -> None:
    tree = ast.parse(inspect.getsource(email_module))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id in {"eval", "exec", "compile"}:
                pytest.fail(f"verbotener dynamischer Aufruf: {func.id}")
            if isinstance(func, ast.Attribute) and func.attr in {"__import__", "import_module"}:
                pytest.fail(f"verbotener dynamischer Import: {func.attr}")
