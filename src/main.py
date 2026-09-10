from datetime import datetime
from pathlib import Path
from typing import Annotated

import openai
import questionary
import typer
from pydantic import ValidationError
from rich.console import Console
from rich.table import Table

from hirnkastl import consts, utils, validators
from hirnkastl.cards import BaseCard, CardType, GenericCard, MathCard
from hirnkastl.commands import deck
from hirnkastl.config import Config
from hirnkastl.lang_models import OpenAiModel

app = typer.Typer(
    help="**hirnkastl**: A CLI tool for generating Anki flashcards using AI.",
    rich_markup_mode="markdown",
)

app.add_typer(deck.app, name="deck")

console = Console()


@app.command()
def setup():
    """
    Run the interactive configuration wizard.

    Prompts for your OpenAI API key and preferred model, and saves
    them to the local Hirnkastl configuration file.
    """
    try:
        openai_api_key = questionary.text(
            message="OpenAI API key:",
            validate=validators.validate_nonemtpy_str,
        ).unsafe_ask()

        openai_model = questionary.text(
            message="OpenAI model:",
            validate=validators.validate_nonemtpy_str,
            default="gpt-5.4-2026-03-05",
        ).unsafe_ask()

        config = Config.from_default(
            openai_api_key=openai_api_key,
            openai_model=openai_model,
        )
        utils.save_config(config)

        console.print(
            f"[bold green]SUCCESS:[/bold green] Setup complete! The config was saved to: {consts.CONFIG_FILE}"
        )
    except KeyboardInterrupt:
        console.print("\nAborted")
        raise typer.Exit(code=0)


def display_cards(cards: list[BaseCard]) -> None:
    if not cards:
        console.print("[yellow]WARNING:[/yellow] No cards to display.")
        return

    card_type = type(cards[0])

    # configure table header
    table = Table()
    table.add_column("Number", style="dim")

    if card_type is GenericCard:
        table.add_column("Question", style="white", ratio=1)
        table.add_column("Answer", style="white", ratio=2)
    elif card_type is MathCard:
        table.add_column("Category", style="bold green")
        table.add_column("Question", style="white", ratio=1)
        table.add_column("Question", style="white", ratio=2)
        table.add_column("Topic", style="bold blue")
    else:
        raise TypeError(f"Unknown type: {card_type}")

    # populate table
    for idx, card in enumerate(cards):
        if type(card) is GenericCard:
            table.add_row(
                str(idx),
                card.question,
                card.answer,
            )
        elif type(card) is MathCard:
            table.add_row(
                str(idx),
                card.category,
                card.question,
                card.answer,
                card.topic,
            )
        else:
            raise TypeError(f"Unknown type: {card_type}")

    console.print(table)


@app.command()
def gen(
    deck_name: str = typer.Argument(
        metavar="DECK",
        help="The name of the target Anki deck (must exist in your local decks).",
    ),
    card_type: CardType = typer.Argument(
        help="The structural schema for the flashcards (e.g., 'math' or 'generic').",
    ),
    file: Path = typer.Argument(
        help="Path to the source document to extract knowledge from or cache file in case the `--from-cache` flag is used.",
    ),
    comment: str | None = typer.Option(
        default=None,
        help="Custom instructions for the AI prompt (e.g., 'Focus only on definitions').",
    ),
    skip_review: bool = typer.Option(
        is_flag=True,
        default=False,
        help="Bypass the interactive table preview and generate the Anki package immediately.",
    ),
    export_name: str = typer.Option(
        callback=validators.validate_export_name,
        default_factory=utils.gen_export_name,
        help="Custom filename for the generated .apkg file (without extension).",
    ),
    tags: list[str] = typer.Option(
        default_factory=list,
        callback=validators.validate_tags,
        help="Tags to apply to the generated cards (spaces are automatically converted to underscores).",
    ),
    open: bool = typer.Option(
        default=False,
        is_flag=True,
        help="Open the generated .apkg file after generation for importing into Anki.",
    ),
    from_cache: bool = typer.Option(
        default=False,
        is_flag=True,
        help="Load the last generated cards from the local cache instead of calling the AI.",
    ),
):
    """
    Generate Anki flashcards from a document using AI.

    Parses the target document using your configured OpenAI model, applies
    the selected card schema, and compiles an importable Anki package (.apkg).
    """
    # 0. PREPARATION
    # load decks
    decks = utils.load_decks()

    # check if deck exists
    if deck_name not in decks:
        utils.abort_with_error(f"A deck with the name {deck_name} does not exist.")
    deck = decks[deck_name]

    # check if file exists
    if not file or not file.exists():
        utils.abort_with_error("The specified document path does not exist.")

    cards = []
    if from_cache:
        # 1.A. LOAD FROM CACHE FILE IF GIVEN
        try:
            cards = utils.load_cards_from_file(file, card_type)
            console.print(
                f"[bold green]INFO:[/bold green] Loaded {len(cards)} cards from cache."
            )
        except Exception as e:
            utils.abort_with_error(f"Failed to load cache: {e}")
    else:
        # 1.B. GENERATE USING LLM
        # configure model
        model = OpenAiModel()

        # add model tag
        tags.append(f"hirnkastl::{model.model}")

        # generate cards
        try:
            with console.status("Generating flashcards...", spinner="dots"):
                cards = model.generate_cards(card_type, file, comment)  # type: ignore
        except openai.AuthenticationError:
            utils.abort_with_error(
                "Invalid OpenAI API key. Please run [cyan]hirnkastl setup[/cyan] to reconfigure your key."
            )
        except openai.RateLimitError:
            utils.abort_with_error(
                "OpenAI rate limit exceeded or insufficient account balance. Please check your billing dashboard."
            )
        except openai.APIConnectionError:
            utils.abort_with_error(
                "Failed to connect to the OpenAI API. Please check your internet connection."
            )
        except ValidationError as e:
            utils.abort_with_error(
                f"The AI generated malformed data that couldn't be parsed.\n[dim]{e}[/dim]"
            )
        except Exception as e:
            utils.abort_with_error(str(e))

    # 2. REVIEW CARDS
    if not skip_review:
        display_cards(cards)
        add_to_deck: bool = questionary.confirm(
            "Do you want to add these cards to your deck?",
            default=True,
        ).ask()

        if not add_to_deck:
            # save cards to cache file for later import
            consts.CACHE_DIR.mkdir(parents=True, exist_ok=True)
            cache_file = consts.CACHE_DIR / f"{export_name}.json"
            cache_file_uri = cache_file.resolve().as_uri()

            utils.save_cards_to_file(cards, cache_file)

            console.print(
                "[yellow]Aborted. Cards have NOT been added to the deck.[/yellow]\n"
                f"[dim]Your generated cards have been saved to cache: [link={cache_file_uri}][cyan]{cache_file.resolve()}[/cyan][/link]\n"
                "You can review or import them later using:[/dim]\n"
                f"[cyan]hirnkastl gen ... --cache-file {cache_file.resolve()}[/cyan]"
            )
            raise typer.Exit(code=0)

    # 3. ADD TO DECK
    anki_deck = utils.deck_to_anki_deck(deck)
    for card in cards:
        note = utils.card_to_anki_note(card, export_name, tags)
        anki_deck.add_note(note)

    # 4. EXPORT
    export_path = consts.EXPORTS_DIR / f"{export_name}.apkg"
    utils.export_anki_deck(anki_deck, export_path)
    export_path_uri = export_path.resolve().as_uri()
    console.print(
        f"[bold green]SUCCESS:[/bold green] The Anki package was generated and saved to: [link={export_path_uri}][cyan]{export_path.resolve()}[/cyan][/link]\n"
        "[dim]Open Anki and import this file to load your cards. If your terminal supports it, you can click the link above to automatically start the import process.[/dim]"
    )

    # open file to start import
    if open:
        typer.launch(str(export_path.resolve()))


if __name__ == "__main__":
    app()
