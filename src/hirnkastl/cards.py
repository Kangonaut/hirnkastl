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
    PROOF_IDEA = "proof_idea"
    EXERCISE = "exercise"


class MathCard(BaseCard):
    category: MathCardCategory = Field(
        description="theorem, definition, proof idea, or exercise"
    )
    question: str = Field(description="the front side of the card")
    answer: str = Field(description="the back side of the card")
    topic: str


class CardType(str, Enum):
    GENERIC = "generic"
    MATH = "math"
