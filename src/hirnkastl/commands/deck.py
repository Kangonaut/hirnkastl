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
    name: str,
    description: str = Argument(default=""),
):
    decks = utils.load_decks()

    # check for unique name
    if name in decks:
        console.print(
            f"[bold red]Error:[/bold red] A deck named [cyan]{name}[/cyan] already exists."
        )
        raise typer.Exit(code=1)

    deck = Deck(deck_id=utils.gen_anki_id(), name=name, description=description)
    decks[name] = deck
    utils.save_decks(decks)

    console.print(f"Entry saved. New deck count: {len(decks)}.")


@app.command("list")
def list_decks():
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
