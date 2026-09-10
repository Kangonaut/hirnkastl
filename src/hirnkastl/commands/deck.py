from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table
from typer.params import Argument

from hirnkastl import utils
from hirnkastl.decks import Deck

app = typer.Typer(help="Manage flashcard decks.")

console = Console()


@app.command("add")
def add_deck(
    name: str = typer.Argument(
        help="The unique name for the new deck.",
    ),
    description: str = typer.Argument(
        default="",
        help="An optional description of the deck's contents.",
    ),
):
    """
    Create a new Anki deck profile.

    Registers a new deck with a unique ID in your local configuration,
    which can then be used as a target for generating flashcards.
    """
    decks = utils.load_decks()

    # check for unique name
    if name in decks:
        utils.abort_with_error(f"A deck named [cyan]{name}[/cyan] already exists.")

    deck = Deck(deck_id=utils.gen_anki_id(), name=name, description=description)
    decks[name] = deck
    utils.save_decks(decks)

    console.print(f"Entry saved. New deck count: {len(decks)}.")


@app.command("list")
def list_decks():
    """
    List all configured Anki decks.

    Displays a table of all locally saved decks, including their
    unique IDs, names, and descriptions.
    """
    decks = list(utils.load_decks().values())
    decks.sort(key=lambda d: d.name)

    if not decks:
        console.print(
            "[yellow]No decks found. Create one using 'hirnkastl decks add'.[/yellow]"
        )
        return

    table = Table(box=None)
    table.add_column("ID", style="dim", width=12)
    table.add_column("Name", style="bold green")
    table.add_column("Description", style="white")

    for deck in decks:
        table.add_row(
            str(deck.deck_id),
            deck.name,
            deck.description or "[italic dim]-[/italic dim]",
        )

    console.print(table)
