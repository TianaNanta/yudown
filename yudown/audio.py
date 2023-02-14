import typer
from pytube import YouTube

app = typer.Typer()

@app.callback()
def main(
    url: str = typer.Argument(..., help="Youtube link of the [bold red]Audio[/bold red] to download", show_default=False)
    ):
    """ Download Youtube [green]Audio[/green] 🎤"""
    return

@app.command("down")
def single_download(url: str = typer.Argument(...)):
    url = typer.prompt("Youtube audio link")
    return