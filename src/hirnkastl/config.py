from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from hirnkastl import consts, utils

DEFAULT_VALUE_REGISTRY: dict[str, Any] = {
    "card_prompts": consts.DEFAULT_CARD_PROMPTS,
}


class Config(BaseSettings):
    openai_api_key: str
    openai_model: str
    card_prompts: dict[str, str] = Field(default_factory=dict)

    model_config = SettingsConfigDict(env_file=None)

    @classmethod
    def from_default(cls, **args):
        # replace missing fields with defaults
        for field, value in DEFAULT_VALUE_REGISTRY.items():
            if field not in args:
                args[field] = value

        return Config(**args)


_settings = None


def __getattr__(name: str):
    # lazy load settings
    global _settings
    if name == "settings":
        if _settings is None:
            _settings = utils.load_config()
        return _settings
    raise AttributeError(f"Module {__name__!r} has no attribute {name}.")
