import base64
from pathlib import Path

import filetype


def file_to_base64(path: Path) -> str:
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def get_file_mime(path: Path) -> str:
    kind = filetype.guess(path)
    return kind.mime
