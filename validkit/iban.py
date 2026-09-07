"""IBAN-Validierung (Modulo-97)."""

_MAX_INPUT_LEN = 10000
_MIN_IBAN_LEN = 15
_MAX_IBAN_LEN = 34


def is_valid_iban(text: str) -> bool:
    """Prüfe, ob *text* eine syntaktisch gültige IBAN ist.

    Die Prüfung normalisiert die Eingabe (Großschreibung, Entfernen von
    Leerzeichen und Bindestrichen), verschiebt die ersten vier Zeichen ans
    Ende, wandelt Buchstaben in Ziffern um und prüft den Rest bei Division
    durch 97: gültig genau dann, wenn der Rest 1 ist.

    Offensichtlich ungültige Längen oder Zeichen werden vorab abgelehnt.
    Eingaben über 10.000 Zeichen werden sofort mit ``False`` abgelehnt, bevor
    die Musterprüfung beginnt. Eine leere Eingabe oder eine Eingabe mit
    unzulässigen Zeichen löst ``ValueError`` aus; ein falscher Typ
    ``TypeError``. Die Fehlermeldung nennt nur den Funktionsnamen und den
    Ablehnungsgrund, niemals den Eingabewert.
    """
    if not isinstance(text, str):
        raise TypeError("is_valid_iban: erwartet einen String")
    if len(text) > _MAX_INPUT_LEN:
        return False

    normalized = text.upper().replace(" ", "").replace("-", "")

    if not normalized:
        raise ValueError("is_valid_iban: Eingabe darf nicht leer sein")
    if not normalized.isascii() or not normalized.isalnum():
        raise ValueError("is_valid_iban: Eingabe enthält unzulässige Zeichen")
    if not _MIN_IBAN_LEN <= len(normalized) <= _MAX_IBAN_LEN:
        return False
    if not normalized[:2].isalpha() or not normalized[2:4].isdigit():
        return False

    rearranged = normalized[4:] + normalized[:4]

    remainder = 0
    for char in rearranged:
        if char.isdigit():
            remainder = (remainder * 10 + int(char)) % 97
        else:
            remainder = (remainder * 100 + (ord(char) - 55)) % 97

    return remainder == 1
