"""E-Mail-Validierung."""

import re

_MAX_LENGTH = 10000

# Genau ein @, nicht-leerer lokaler Teil, Domain mit mindestens einem Punkt.
# Keine verschachtelten Quantoren: `+` wirkt nur auf Zeichenklassen, nie auf
# eine Gruppe, daher terminiert die Prüfung auch bei langen Eingaben linear.
_EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def is_valid_email(text: str) -> bool:
    """Prüfe, ob *text* eine syntaktisch gültige E-Mail-Adresse ist.

    Gültig ist eine Adresse mit genau einem ``@``, einem nicht-leeren lokalen
    Teil und einer Domain, die einen Punkt enthält. Eingaben über
    ``_MAX_LENGTH`` Zeichen werden unmittelbar mit ``False`` abgelehnt, bevor
    die Musterprüfung beginnt. Ein falscher Typ führt zu ``TypeError``.
    """
    if not isinstance(text, str):
        raise TypeError("is_valid_email: text muss ein str sein")
    if len(text) > _MAX_LENGTH:
        return False
    return _EMAIL_RE.fullmatch(text) is not None
