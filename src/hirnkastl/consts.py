import genanki
from platformdirs import PlatformDirs

from hirnkastl.cards import CardType, GenericCard, MathCard

dirs = PlatformDirs(appname="hirnkastl")

CARD_CSS = """
.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 16px;
    color: #24292e;
    background-color: #ffffff;
    line-height: 1.5;
    padding: 24px;
    max-width: 650px;
    margin: 0 auto;
}
.topic {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #6a737d;
    margin-bottom: 6px;
    font-weight: 600;
}
.badge {
    display: inline-block;
    padding: 3px 8px;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 4px;
    background-color: #e1edf8;
    color: #0366d6;
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}
.question {
    font-weight: 600;
    font-size: 1.15rem;
    color: #24292e;
    margin-bottom: 16px;
}
hr {
    border: none;
    border-top: 1px solid #eaecef;
    margin: 20px 0;
}
.answer {
    color: #24292e;
}
"""

CARD_TYPE_CLASSES = {
    CardType.GENERIC: GenericCard,
    CardType.MATH: MathCard,
}

CARD_TYPE_ANKI_MODELS = {
    CardType.GENERIC: genanki.Model(
        model_id=1715196275,
        name="hirnkastl - generic model",
        fields=[
            {"name": "Topic"},
            {"name": "Question"},
            {"name": "Answer"},
        ],
        templates=[
            {
                "name": "Card",
                "qfmt": '<div class="topic">{{Topic}}</div><div class="question">{{Question}}</div>',
                "afmt": '{{FrontSide}}<hr><div class="answer">{{Answer}}</div>',
            }
        ],
        css=CARD_CSS,
    ),
    CardType.MATH: genanki.Model(
        model_id=1340923860,
        name="hirnkastl - math model",
        fields=[
            {"name": "Topic"},
            {"name": "Category"},
            {"name": "Question"},
            {"name": "Answer"},
        ],
        templates=[
            {
                "name": "Math Card",
                "qfmt": '<div class="topic">{{Topic}}</div><div class="badge">{{Category}}</div><div class="question">{{Question}}</div>',
                "afmt": '{{FrontSide}}<hr><div class="answer">{{Answer}}</div>',
            }
        ],
        css=CARD_CSS,
    ),
}


CONFIG_FILE = dirs.user_config_path / "config.yaml"

DECKS_CACHE_FILE = dirs.user_cache_path / "decks.yaml"

EXPORTS_DIR = dirs.user_data_path / "exports"

DEFAULT_CARD_PROMPTS = {
    "math": "You are a mathematics professor assistant. Extract fundamental definitions, core theorems, proof ideas, and exercises. Use LaTeX formatting.",
    "language": "You are an instructor. Extract the most important information into flashcards.",
    "code": "You are a computer science professor assistant. Extract concise, self-contained code snippets featuring execution logic or bugs, with step-by-step memory traces.",
}

SUPPORTED_FILE_TYPES = {
    "application/pdf",
    "text/plain",
    "text/markdown",
}
