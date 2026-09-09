import questionary
import typer
from rich.console import Console
from rich.table import Table

from hirnkastl import commands, consts, utils, validators
from hirnkastl.commands import deck
from hirnkastl.config import Config

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


if __name__ == "__main__":
    app()
