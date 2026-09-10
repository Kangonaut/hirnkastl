import re

import typer


def validate_nonemtpy_str(text: str) -> bool | str:
    if not text.strip():
        return "Cannot be empty."
    return True


def validate_export_name(value: str) -> str:
    """Ensures the export_name contains no spaces and match an alphanumeric pattern (with optional hyphens/colons)."""
    pattern = re.compile(r"^[a-zA-Z0-9_:-]+$")

    if not pattern.match(value):
        raise typer.BadParameter(
            f"Invalid export_name format: '{value}'. Cannot contain spaces and must use only letters, numbers, underscores, hyphens, or colons."
        )

    return value


def validate_tags(values: list[str]) -> list[str]:
    """Ensures tags contain no spaces and match an alphanumeric pattern (with optional hyphens/colons)."""
    pattern = re.compile(r"^[a-zA-Z0-9_:\.-]+$")

    for tag in values:
        if not pattern.match(tag):
            raise typer.BadParameter(
                f"Invalid tag format: '{tag}'. Tags cannot contain spaces and must use only letters, numbers, underscores, hyphens, colons and dots."
            )

    return values
