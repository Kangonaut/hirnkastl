def validate_nonemtpy_str(text: str) -> bool | str:
    if not text.strip():
        return "Cannot be empty."
    return True
