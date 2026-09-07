"""Maskierung von Geheimnissen."""


def mask_secret(text: str, keep: int = 4) -> str:
    """Maske *text* und lasse nur die letzten *keep* Zeichen unverändert."""
    if not isinstance(text, str):
        raise TypeError("mask_secret: text must be a string")
    if not isinstance(keep, int):
        raise TypeError("mask_secret: keep must be an integer")
    if keep < 0 or keep > len(text):
        raise ValueError("mask_secret: keep must be between 0 and the text length")
    return "*" * (len(text) - keep) + text[len(text) - keep :]
