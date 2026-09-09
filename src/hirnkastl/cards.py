from enum import Enum

from openai import BaseModel
from pydantic import Field


class Flashcard(BaseModel):
    pass


class GenericCard(Flashcard):
    question: str = Field(description="the front side of the card")
    answer: str = Field(description="the back side of the card")
    topic: str


class CodeTracingCard(Flashcard):
    programming_language: str = Field(
        description="The language of the snippet, e.g., 'python', 'cpp', 'java'"
    )
    code_snippet: str = Field(
        description="A concise, self-contained code block featuring tricky behavior, state mutation, or a hidden bug."
    )
    question: str = Field(
        description="The task, e.g., 'What is the exact output?' or 'Identify the bug and state the correct output.'"
    )
    solution_explanation: str = Field(
        description="Step-by-step memory trace or execution explanation detailing why the code behaves this way."
    )
    concept_tag: str = Field(
        description="Core concept, e.g., 'Recursion', 'Closures', 'Pointer Arithmetic', 'Async Concurrency'"
    )


class MathCardCategory(str, Enum):
    DEFINITION = "definition"
    THEOREM = "theorem"
    PROOF_IDEA = "proof_idea"
    EXERCISE = "exercise"


class MathCard(Flashcard):
    category: MathCardCategory = Field(
        description="theorem, definition, proof idea, or exercise"
    )
    question: str = Field(description="the front side of the card")
    answer: str = Field(description="the back side of the card")
    topic: str
