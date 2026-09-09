from pydantic import BaseModel, Field


class Deck(BaseModel):
    deck_id: int
    name: str
    description: str = Field(default="")
