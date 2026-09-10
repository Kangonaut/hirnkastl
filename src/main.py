from pathlib import Path

import questionary
import typer
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
    try:
        openai_api_key = questionary.text(
            message="OpenAI API key:",
            validate=validators.validate_nonemtpy_str,
        ).unsafe_ask()

        openai_model = questionary.text(
            message="OpenAI model:",
            validate=validators.validate_nonemtpy_str,
            default="gpt-4o",
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
        table.add_column("Question", style="white")
        table.add_column("Answer", style="white")
    elif card_type is MathCard:
        table.add_column("Category", style="bold green")
        table.add_column("Question", style="white")
        table.add_column("Question", style="white")
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
    deck_name: str = typer.Argument(metavar="DECK"),
    card_type: CardType = typer.Argument(),
    document: Path = typer.Argument(),
    comment: str | None = typer.Option(default=None),
    skip_review: bool = typer.Option(is_flag=True, default=False),
    export_name: str | None = typer.Option(default=None),
):
    decks = utils.load_decks()

    # check if deck exists
    if deck_name not in decks:
        console.print(
            f"[bold red]ERROR:[/bold red] A deck with the name {deck_name} does not exist."
        )
        raise typer.Exit(code=1)
    deck = decks[deck_name]

    # check if file exists
    if not document.exists():
        console.print(
            f"[bold red]ERROR:[/bold red] The specified document path does not exist."
        )
        raise typer.Exit(code=1)

    # generate cards
    with console.status("Generating flashcards...", spinner="dots"):
        model = OpenAiModel()
        cards = model.generate_cards(card_type, document, comment)

    # review cards
    if not skip_review:
        display_cards(cards)
        add_to_deck: bool = questionary.confirm(
            "Do you want to add these cards to your deck?",
            default=True,
        ).ask()

        if not add_to_deck:
            console.print(
                "[yellow]Aborted. Cards have NOT been added to the deck.[/yellow]"
            )
            # TODO: save cards list in a subdirectory of the cache folder
            raise typer.Exit(code=0)

    # add cards to deck
    anki_deck = utils.deck_to_anki_deck(deck)
    for card in cards:
        note = utils.card_to_anki_note(card)
        anki_deck.add_note(note)

    # export
    export_path = utils.export_anki_deck(anki_deck, export_name)
    export_path_uri = export_path.resolve().as_uri()
    console.print(
        f"[bold green]SUCCESS:[/bold green] The Anki package was generated and saved to: [link={export_path_uri}][cyan]{export_path.resolve()}[/cyan][/link]\n"
        "[dim]Open Anki and import this file to load your cards.[/dim]"
    )


if __name__ == "__main__":
    app()
