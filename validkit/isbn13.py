"""ISBN-13-Validierung."""

_MAX_LENGTH = 10000


def is_valid_isbn13(text: str) -> bool:
    """Prüfe, ob *text* eine gültige ISBN-13 ist."""
    if not isinstance(text, str):
        raise TypeError("is_valid_isbn13: input must be a string")
    if len(text) > _MAX_LENGTH:
        return False
    digits = text.replace("-", "").replace(" ", "")
    if digits and not digits.isdecimal():
        raise ValueError("is_valid_isbn13: contains non-digit characters")
    if len(digits) != 13:
        return False
    total = 0
    for index, char in enumerate(digits):
        weight = 1 if index % 2 == 0 else 3
        total += int(char) * weight
    return total % 10 == 0
