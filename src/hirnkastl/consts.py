from platformdirs import PlatformDirs

from hirnkastl.cards import CodeTracingCard, GenericCard, MathCard

dirs = PlatformDirs(appname="hirnkastl")

CARD_CLASS_REGISTRY = {
    "generic": GenericCard,
    "math": MathCard,
    "code-tracing": CodeTracingCard,
}


CONFIG_FILE = dirs.user_config_path / "config.yaml"

DECKS_CACHE_FILE = dirs.user_cache_path / "decks.yaml"

DEFAULT_CARD_PROMPTS = {
    "math": "You are a mathematics professor assistant. Extract fundamental definitions, core theorems, proof ideas, and exercises. Use LaTeX formatting.",
    "language": "You are an instructor. Extract the most important information into flashcards.",
    "code": "You are a computer science professor assistant. Extract concise, self-contained code snippets featuring execution logic or bugs, with step-by-step memory traces.",
}
