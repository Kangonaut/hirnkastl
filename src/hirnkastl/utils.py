import base64
import random
from pathlib import Path

import filetype


def get_new_anki_id() -> int:
    return random.randrange(1 << 30, 1 << 31)


def file_to_base64(path: Path) -> str:
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def get_file_mime(path: Path) -> str:
    kind = filetype.guess(path)
    if kind is None:
        raise Exception(f"Cannot infer file type of {path}")
    return kind.mime
