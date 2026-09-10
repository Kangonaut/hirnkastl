from abc import ABC, abstractmethod
from pathlib import Path

from openai import OpenAI
from pydantic import BaseModel, create_model

from hirnkastl import consts, utils
from hirnkastl.cards import BaseCard, CardType
from hirnkastl.config import settings


class AbstractLangModel(ABC):
    @abstractmethod
    def generate[T: BaseModel](
        self,
        instruction: str,
        document: Path,
        response_class: type[T],
        comment: str | None = None,
    ) -> T:
        pass

    def generate_cards(
        self,
        card_type: CardType,
        document: Path,
        comment: str | None = None,
    ) -> list[BaseCard]:
        card_class = utils.get_card_class_from_type(card_type)
        response_class = create_model(
            "BatchResponseModel",
            cards=(list[card_class], ...),
        )

        instruction = settings.card_prompts[card_type.value]

        response = self.generate(instruction, document, response_class, comment)
        return response.cards  # type: ignore


class OpenAiModel(AbstractLangModel):
    def __init__(
        self,
        api_key: str = settings.openai_api_key,
        model: str = settings.openai_model,
    ):
        self.model = model
        self.client = OpenAI(api_key=api_key)

    def generate[T: BaseModel](
        self,
        instruction: str,
        document: Path,
        response_class: type[T],
        comment: str | None = None,
    ) -> T:
        print(f"response class: {response_class}")

        file_mime = utils.get_file_mime(document)
        file_content = utils.file_to_base64(document)

        if file_mime not in consts.SUPPORTED_FILE_TYPES:
            raise Exception(f"Unsupported attachment file type: {file_mime}")

        response = self.client.responses.parse(
            model=self.model,
            instructions=instruction,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_file",
                            "filename": document.name,
                            "file_data": f"data:{file_mime};base64,{file_content}",
                        },
                        {
                            "type": "input_text",
                            "text": comment or "",
                        },
                    ],
                }
            ],
            text_format=response_class,
        )

        if not response.output_parsed:
            raise Exception(f"Model did not return a valid response. Please try again.")

        return response.output_parsed
