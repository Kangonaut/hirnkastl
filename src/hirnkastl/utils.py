import base64
import random
from datetime import datetime
from pathlib import Path
from typing import TypeVar

import filetype
import genanki
import yaml
from pydantic import BaseModel, TypeAdapter
from pydantic_settings import BaseSettings

from hirnkastl import consts
from hirnkastl.cards import BaseCard, CardType, GenericCard, MathCard
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


def get_card_class_from_type(card_type: CardType) -> type:
    return consts.CARD_TYPE_CLASSES[card_type]


def card_to_anki_note(card: BaseCard) -> genanki.Note:
    if isinstance(card, MathCard):
        return genanki.Note(
            model=consts.CARD_TYPE_ANKI_MODELS[CardType.MATH],
            fields=[
                card.topic,
                card.category.value,
                card.question,
                card.answer,
            ],
        )
    elif isinstance(card, GenericCard):
        return genanki.Note(
            model=consts.CARD_TYPE_ANKI_MODELS[CardType.GENERIC],
            fields=[
                card.topic,
                card.question,
                card.answer,
            ],
        )
    raise TypeError(f"Unsupported card type for Anki export: {type(card)}")


def deck_to_anki_deck(deck: Deck) -> genanki.Deck:
    return genanki.Deck(
        deck_id=deck.deck_id,
        name=f"hirnkastl::{deck.name}",
        description=deck.description,
    )


def export_anki_deck(deck: genanki.Deck, export_name: str | None = None) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = consts.EXPORTS_DIR / f"{export_name or f"hirnkastl-export-{timestamp}"}.apkg"
    path.parent.mkdir(parents=True, exist_ok=True)

    genanki.Package(deck).write_to_file(path)
    return path
