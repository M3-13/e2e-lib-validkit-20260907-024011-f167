"""Slug-Erzeugung."""

import re
import unicodedata

_MAX_LENGTH = 10_000

_NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Wandle *text* in einen URL-freundlichen Slug um.

    Kleinschreibung, Entfernung diakritischer Zeichen, Ersetzung aller
    nicht-alphanumerischen Zeichen durch einen Bindestrich sowie das
    Zusammenfassen mehrfacher Bindestriche. Führende und abschließende
    Bindestriche werden entfernt.
    """
    if not isinstance(text, str):
        raise TypeError("slugify: erwartet einen String")
    if len(text) > _MAX_LENGTH:
        raise ValueError("slugify: Eingabe überschreitet die maximale Länge")

    decomposed = unicodedata.normalize("NFKD", text)
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    lowered = stripped.lower().replace("\u00df", "ss")
    return _NON_ALNUM_RE.sub("-", lowered).strip("-")
