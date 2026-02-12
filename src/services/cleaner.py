from src.core.config import IGNORE_PATTERNS

def clean_filename(filename: str) -> str:
    """Remove specific strings from the filename."""
    cleaned = filename
    for pattern in IGNORE_PATTERNS:
        cleaned = cleaned.replace(pattern, "")
    return cleaned
