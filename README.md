<div align="center">
<img src="assets/icon.jpeg" alt="icon" width="192"/>

# hirnkastl

[![license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/Kangonaut/hirnkastl/blob/main/LICENSE)

</div>

# hirnkastl

**hirnkastl** is a powerful command-line interface (CLI) tool that uses AI to automatically generate structured Anki flashcards from your study documents, lecture notes, and math scripts. Built with Python, Typer, Rich, and OpenAI.

## Features

- **AI-Powered Generation:** Upload raw PDFs or study materials and let OpenAI parse them into structured flashcards.
- **Schema Support:** Out-of-the-box support for different card formats (e.g., **Generic** questions/answers and **Math** cards equipped with categories like definitions, theorems, and exercises).
- **Interactive Review:** Inspect generated flashcards in a neatly formatted terminal table before committing them to your deck.
- **Smart Caching:** Aborted a review? Hirnkastl automatically caches your generated cards so you don't lose progress or waste API credits. Re-import them anytime using `--from-cache`.
- **Native Anki Packages (`.apkg`):** Compiles standard Anki package files that are 100% stable, requiring zero fragile local API add-ons.
- **Auto-Import Option:** Automatically open the generated `.apkg` file with your operating system's default handler to jump straight into Anki.

## Installation

Clone the repository and install the project using your preferred Python package manager (e.g., Poetry or pip):

```bash
git clone https://github.com/your-username/hirnkastl.git
cd hirnkastl
pip install .

```

## Installation

Hirnkastl uses `uv`.

### 1. Install `uv` (if not already installed)

On macOS and Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

```

On Windows:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

```

### 2. Clone and Install Hirnkastl

Clone the repository and install the tool globally using `uv` so it's accessible anywhere in your terminal:

```bash
git clone https://github.com/your-username/hirnkastl.git
cd hirnkastl
uv tool install .

```

If you prefer to run it in development mode without a global install, use `uv sync` followed by `uv run hirnkastl`:

```bash
uv sync
uv run hirnkastl --help

```

## Setup

Before generating cards, configure your OpenAI API key and preferred model by running the interactive setup wizard:

```bash
hirnkastl setup

```

## Usage

### 1. Manage Decks

Before generating cards, create a local target deck:

```bash
# Add a new deck
hirnkastl decks add math-deck "Advanced mathematics lecture notes"

# List all local decks
hirnkastl decks list

```

### 2. Generate Flashcards

Run the `gen` command by passing your target deck name, card schema type, and path to your PDF document:

```bash
hirnkastl gen math-deck math skriptum-ausschnitt.pdf --tags algebra --tags exam-prep --comment "Focus heavily on vector spaces"

```

## (Hopefully) Upcoming Features

- [ ] estimate the cost of a request based on the provided document using `tiktoken` and the configured model
- [ ] more card types:
  - [ ] languages
  - [ ] coding

## Upcoming Improvements

- [x] store the flashcards in the cache directory for later import (maybe using `hirnkastl gen --from-cache`), when the user decides not to import the generated flashcards
- [ ] store prompts in separate config files
- [ ] complete CRUD operations for decks (so update and delete)
- [ ] add default card_type to the deck

## License

Distributed under the [Apache License 2.0](https://github.com/Kangonaut/hirnkastl/blob/main/LICENSE).

---

<div align="center">
<a href="https://www.buymeacoffee.com/kangonaut" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
</div>
