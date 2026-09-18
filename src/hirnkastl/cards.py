from abc import ABC
from enum import Enum

from pydantic import BaseModel, Field


class BaseCard(BaseModel, ABC):
    pass


class GenericCard(BaseCard):
    question: str = Field(description="the front side of the card")
    answer: str = Field(description="the back side of the card")
    topic: str


class MathCardCategory(str, Enum):
    DEFINITION = "definition"
    THEOREM = "theorem"
    PROOF = "proof"
    EXERCISE = "exercise"
    CONCEPTUAL = "conceptual"


class MathCard(BaseCard):
    question: str = Field(description="the front side of the card")
    answer: str = Field(description="the back side of the card")
    category: MathCardCategory = Field(
        description="theorem, definition, exercise or conceptual"
    )
    topic: str


class CardType(str, Enum):
    GENERIC = "generic"
    MATH = "math"
