"""Akzent-Entfernung."""

import unicodedata


def strip_accents(text: str) -> str:
    """Entferne diakritische Zeichen aus *text*.

    Zerlegt den Text per NFD-Normalisierung in Grundbuchstaben und
    Kombinationszeichen und entfernt anschließend alle Kombinationszeichen,
    sodass lateinische Buchstaben mit diakritischen Zeichen in ihre Grundform
    überführt werden, ohne andere Zeichen zu verändern.
    """
    if not isinstance(text, str):
        raise TypeError("strip_accents: text must be a str")
    return "".join(
        char for char in unicodedata.normalize("NFD", text) if unicodedata.category(char) != "Mn"
    )
