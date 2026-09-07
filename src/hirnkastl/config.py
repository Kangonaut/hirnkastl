import yaml
from platformdirs import PlatformDirs
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich import print

dirs = PlatformDirs(appname="hirnkastl")

CONFIG_FILE = dirs.user_config_path / "config.yaml"


class Config(BaseSettings):
    openai_api_key: str
    openai_model: str
    flashcard_instruction: str

    model_config = SettingsConfigDict(env_file=None)


def load_config() -> Config:
    if not CONFIG_FILE.exists():
        print("Config file does not exist. Please run `hirnkastl setup` first.")
        raise SystemExit(1)

    with open(CONFIG_FILE, "r") as file:
        return Config.model_validate(yaml.safe_load(file))


_settings = None


def __getattr__(name: str):
    # lazy load settings
    global _settings
    if name == "settings":
        if _settings is None:
            _settings = load_config()
        return _settings
    raise AttributeError(f"Module {__name__!r} has no attribute {name}.")
