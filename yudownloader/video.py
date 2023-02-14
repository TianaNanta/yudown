import typer

app = typer.Typer()

@app.callback()
def main(
    url: str = typer.Argument(..., help="Youtube link of the [bold red]Video[/bold red] to download", show_default=False)
    ):
    """ Download Youtube [red]Video[/red] 🎬"""
    return