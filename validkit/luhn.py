"""Luhn-Prüfsumme."""


def luhn_check(digits: str) -> bool:
    """Prüfe, ob *digits* eine gültige Luhn-Prüfsumme besitzt.

    Führende Nullen werden akzeptiert. Eine leere Eingabe oder eine Eingabe,
    die nicht ausschließlich aus ASCII-Ziffern besteht, löst ``ValueError``
    aus; ein falscher Typ ``TypeError``. Die Fehlermeldung nennt nur den
    Funktionsnamen und den Ablehnungsgrund, niemals den Eingabewert.
    """
    if not isinstance(digits, str):
        raise TypeError("luhn_check: erwartet einen String")
    if not digits:
        raise ValueError("luhn_check: Eingabe darf nicht leer sein")
    if not digits.isascii() or not digits.isdigit():
        raise ValueError("luhn_check: Eingabe darf nur Ziffern enthalten")

    total = 0
    for position, char in enumerate(reversed(digits)):
        value = int(char)
        if position % 2 == 1:
            value *= 2
            if value > 9:
                value -= 9
        total += value
    return total % 10 == 0
