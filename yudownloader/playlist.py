import typer

app = typer.Typer()

@app.callback()
def main(
    url: str = typer.Argument(..., help="Youtube link of the [bold red]Playlist[/bold red] to download", show_default=False)
    ):
    """ Download Youtube [yellow]Playlist[/yellow] 🎧"""
    return