import base64
import random
from pathlib import Path
from typing import TypeVar

import filetype
import yaml
from pydantic import BaseModel, TypeAdapter
from pydantic_settings import BaseSettings

from hirnkastl import consts
from hirnkastl.config import Config
from hirnkastl.decks import Deck


def gen_anki_id() -> int:
    return random.randrange(1 << 30, 1 << 31)


def file_to_base64(path: Path) -> str:
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def get_file_mime(path: Path) -> str:
    kind = filetype.guess(path)
    if kind is None:
        raise Exception(f"Cannot infer file type of {path}")
    return kind.mime


T = TypeVar("T", bound=BaseModel | BaseSettings)


def load_pydantic_from_yaml(
    model_class: type[T],
    path: Path,
) -> T:
    with open(path, "r") as file:
        raw = yaml.safe_load(file)
    return model_class.model_validate(raw)


def load_pydantic_list_from_yaml(
    model_class: type[T],
    path: Path,
) -> list[T]:
    with open(path, "r") as file:
        raw = yaml.safe_load(file)
    return TypeAdapter(list[model_class]).validate_python(raw)


def save_pydantic_to_yaml(model: BaseModel, path: Path) -> None:
    with open(path, "w") as file:
        yaml.safe_dump(
            model.model_dump(mode="json"),
            file,
            sort_keys=False,
        )


def save_pydantic_list_to_yaml(
    model: list[T],
    model_class: type[T],
    path: Path,
) -> None:
    data = TypeAdapter(list[model_class]).dump_python(model, mode="json")
    with open(path, "w") as file:
        yaml.safe_dump(
            data,
            file,
            sort_keys=False,
        )


def load_decks(path: Path = consts.DECKS_CACHE_FILE) -> dict[str, Deck]:
    if not path.exists():
        return dict()
    decks = load_pydantic_list_from_yaml(Deck, path)
    return {d.name: d for d in decks}


def save_decks(decks: dict[str, Deck], path: Path = consts.DECKS_CACHE_FILE):
    path.parent.mkdir(parents=True, exist_ok=True)
    save_pydantic_list_to_yaml(list(decks.values()), Deck, path)


def load_config(path: Path = consts.CONFIG_FILE) -> Config:
    if not path.exists():
        print("Config file does not exist. Please run `hirnkastl setup` first.")
        raise SystemExit(1)

    return load_pydantic_from_yaml(Config, path)


def save_config(config: Config, path: Path = consts.CONFIG_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    save_pydantic_to_yaml(config, path)
