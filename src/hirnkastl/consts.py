from pathlib import Path

import genanki
from platformdirs import PlatformDirs

from hirnkastl.cards import CardType, GenericCard, MathCard

dirs = PlatformDirs(appname="hirnkastl")

PROMPTS_DIR = Path(__file__).parent / "prompts"
CACHE_DIR = dirs.user_cache_path
CONFIG_FILE = dirs.user_config_path / "config.yaml"
DECKS_CACHE_FILE = dirs.user_cache_path / "decks.yaml"
EXPORTS_DIR = dirs.user_data_path / "exports"


def _load_card_prompt(card_type: CardType) -> str:
    path = PROMPTS_DIR / f"{card_type.value}.md"
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8").strip()


CARD_CSS = """
/* --- Default Light Mode --- */
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

/* --- Base Badge Styling --- */
.badge {
    display: inline-block;
    padding: 3px 8px;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 4px;
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    /* Default fallback colors */
    background-color: #e1edf8;
    color: #0366d6;
}

/* --- Badge Category Colors (Light Mode) --- */
.badge[data-category="definition"] {
    background-color: #ffeef0;
    color: #d73a49; /* Red */
}
.badge[data-category="theorem"] {
    background-color: #e1edf8;
    color: #0366d6; /* Blue */
}
.badge[data-category="proof_idea"] {
    background-color: #fff5e8;
    color: #e36209; /* Orange */
}
.badge[data-category="exercise"] {
    background-color: #e6ffed;
    color: #28a745; /* Green */
}

/* --- Dark Mode Overrides --- */
.nightMode.card {
    background-color: #0d1117;
    color: #c9d1d9;
}
.nightMode .topic {
    color: #8b949e;
}
.nightMode .question, 
.nightMode .answer {
    color: #c9d1d9;
}
.nightMode hr {
    border-top: 1px solid #30363d;
}

/* --- Badge Category Colors (Dark Mode) --- */
/* Using translucent backgrounds for a cleaner dark mode look */
.nightMode .badge {
    background-color: rgba(56, 139, 253, 0.15);
    color: #58a6ff;
}
.nightMode .badge[data-category="definition"] {
    background-color: rgba(255, 123, 114, 0.15);
    color: #ff7b72;
}
.nightMode .badge[data-category="theorem"] {
    background-color: rgba(56, 139, 253, 0.15);
    color: #58a6ff;
}
.nightMode .badge[data-category="proof_idea"] {
    background-color: rgba(210, 153, 34, 0.15);
    color: #d29922;
}
.nightMode .badge[data-category="exercise"] {
    background-color: rgba(46, 160, 67, 0.15);
    color: #2ea043;
}
"""

CARD_TYPE_CLASSES = {
    CardType.GENERIC: GenericCard,
    CardType.MATH: MathCard,
}

DEFAULT_CARD_PROMPTS = dict()
for card_type in CardType:
    DEFAULT_CARD_PROMPTS[card_type] = _load_card_prompt(card_type)

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
                "qfmt": '<div class="topic">{{Topic}}</div><div class="badge" data-category="{{Category}}">{{Category}}</div><div class="question">{{Question}}</div>',
                "afmt": '{{FrontSide}}<hr><div class="answer">{{Answer}}</div>',
            }
        ],
        css=CARD_CSS,
    ),
}


SUPPORTED_FILE_TYPES = {
    "application/pdf",
    "text/plain",
    "text/markdown",
}
