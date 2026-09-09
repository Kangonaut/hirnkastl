import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, override

from openai import BaseModel, OpenAI

from hirnkastl import utils
from hirnkastl.cards import MathCard
from hirnkastl.config import settings


class AbstractLangModel(ABC):
    @abstractmethod
    def generate(
        self,
        instruction: str,
        attachment_path: Path,
        user_input: str = "",
    ) -> str:
        pass

    def generate_cards(self):


class OpenAiModel(AbstractLangModel):
    SUPPORTED_FILE_TYPES = {
        "application/pdf",
        "text/plain",
        "text/markdown",
    }

    def __init__(
        self,
        api_key: str = settings.openai_api_key,
        model: str = settings.openai_model,
    ):
        self.model = model
        self.client = OpenAI(api_key=api_key)

    def generate(
        self,
        instruction: str,
        attachment_path: Path,
        user_input: str = "",
        response_model,
    ) -> str:

        file_mime = utils.get_file_mime(attachment_path)
        file_content = utils.file_to_base64(attachment_path)

        if file_mime not in self.SUPPORTED_FILE_TYPES:
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
                            "filename": attachment_path.name,
                            "file_data": f"data:{file_mime};base64,{file_content}",
                        },
                        {
                            "type": "input_text",
                            "text": user_input,
                        },
                    ],
                }
            ],
            text_format=MathFlashcardResponse,
        )
        return response.output_parsed
