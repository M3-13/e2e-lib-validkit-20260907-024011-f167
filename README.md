# validkit

Eine kleine, eigenständige Python-Bibliothek, die ausschließlich die
Standardbibliothek nutzt und neun kleine, voneinander unabhängige, reine Prüf-
und Normalisierungsfunktionen bereitstellt: E-Mail-Validierung,
Luhn-Prüfsumme, IBAN-Modulo-97, ISBN-13, Telefonnummer-Normalisierung nach
E.164, Akzent-Entfernung, Maskierung von Geheimnissen, Slug-Erzeugung und
Werte-Begrenzung. Jede Funktion ist sauber typannotiert, meldet ungültige
Eingaben mit einem aussagekräftigen Fehler und besitzt eigene pytest-Unit-Tests.

## Tech-Stack

- **Sprache:** Python
- **Laufzeit:** Python 3.11+
- **Tests:** pytest
- **Abhängigkeiten:** keine (nur Standardbibliothek)

## Installation

```bash
pip install -e .
```

## Tests

```bash
pytest
```

## Verwendung

Alle neun Funktionen werden über das Paket exportiert:

```python
from validkit import (
    is_valid_email,
    luhn_check,
    is_valid_iban,
    is_valid_isbn13,
    normalize_phone,
    strip_accents,
    mask_secret,
    slugify,
    clamp,
)
```

### `is_valid_email(text: str) -> bool`

```python
is_valid_email("user@example.com")  # True
is_valid_email("nicht@")  # False
```

### `luhn_check(digits: str) -> bool`

```python
luhn_check("79927398713")  # True
```

### `is_valid_iban(text: str) -> bool`

```python
is_valid_iban("DE89 3704 0044 0532 0130 00")  # True
```

### `is_valid_isbn13(text: str) -> bool`

```python
is_valid_isbn13("978-3-16-148410-0")  # True
```

### `normalize_phone(text: str, country_code: str) -> str`

```python
normalize_phone("0176 12345678", "DE")  # "+4917612345678"
```

### `strip_accents(text: str) -> str`

```python
strip_accents("Crème brûlée")  # "Creme brulee"
```

### `mask_secret(text: str, keep: int = 4) -> str`

```python
mask_secret("geheim123", 4)  # "*****123"
```

### `slugify(text: str) -> str`

```python
slugify("Héllo Wörld!")  # "hello-world"
```

### `clamp(value, low, high)`

```python
clamp(5, 0, 10)  # 5
clamp(-3, 0, 10)  # 0
clamp(15, 0, 10)  # 10
```
