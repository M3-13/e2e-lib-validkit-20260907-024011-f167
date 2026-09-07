"""Telefonnummer-Normalisierung nach E.164."""

_COUNTRY_CALLING_CODES: dict[str, str] = {
    "DE": "49",
    "AT": "43",
    "CH": "41",
    "FR": "33",
    "IT": "39",
    "NL": "31",
    "ES": "34",
    "PL": "48",
    "BE": "32",
    "DK": "45",
    "SE": "46",
    "NO": "47",
}

_MAX_LENGTH = 10000

_DIGITS = "0123456789"
_SEPARATORS = " \t\r\n-()/."
_DELETE_SEPARATORS = str.maketrans("", "", _SEPARATORS)


def normalize_phone(text: str, country_code: str) -> str:
    """Normalisiere *text* unter Annahme des Ländercodes *country_code* nach E.164.

    Liefert die Nummer im E.164-Format: führendes ``+``, Landesvorwahl, sonst nur
    Ziffern. Eine nationale Vorwahl-Null (Trunk-Präfix) nach der Landesvorwahl wird
    entfernt. Nicht verarbeitbare Eingaben lösen einen ``ValueError`` aus.
    """
    if not isinstance(text, str):
        raise TypeError("normalize_phone: text must be a string")
    if not isinstance(country_code, str):
        raise TypeError("normalize_phone: country_code must be a string")

    if len(text) > _MAX_LENGTH:
        raise ValueError("normalize_phone: input exceeds 10000 characters")

    calling_code = _COUNTRY_CALLING_CODES.get(country_code.upper())
    if calling_code is None:
        raise ValueError("normalize_phone: unsupported country code")

    digits = _extract_digits(text)

    if digits.startswith("00"):
        digits = digits[2:]
        if not digits.startswith(calling_code):
            raise ValueError("normalize_phone: number does not match country code")
        digits = digits[len(calling_code) :]
    elif digits.startswith(calling_code):
        digits = digits[len(calling_code) :]

    digits = digits.lstrip("0")
    if not digits:
        raise ValueError("normalize_phone: number has no significant digits")

    return "+" + calling_code + digits


def _extract_digits(text: str) -> str:
    """Entferne ein führendes ``+`` und übliche Trenner, liefere nur Ziffern zurück."""
    number = text.strip()
    if number.startswith("+"):
        number = number[1:]
    if "+" in number:
        raise ValueError("normalize_phone: number is not processable")
    number = number.translate(_DELETE_SEPARATORS)
    if not number:
        raise ValueError("normalize_phone: number is not processable")
    if any(ch not in _DIGITS for ch in number):
        raise ValueError("normalize_phone: number contains invalid characters")
    return number
