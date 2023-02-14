"""This module provides the YuDownloader CLI."""
# yudownloader/cli.py

from typing import Optional

import typer
from pytube import Playlist, Search, YouTube, exceptions
from pytube.cli import on_progress
from rich import print
from rich.table import Table

from yudownloader import __app_name__, __version__
from yudownloader.database import create, delete, read
from yudownloader.model import Media

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        # typer.echo(f"{__app_name__} v{__version__}")
        print(f"[bold red]{__app_name__}[/bold red] [green]v{__version__}[/green]")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return

@app.command(short_help="Show the download history")
def history():
    media = read()

    print("📜", "[bold magenta]Download History[/bold magenta]", "📜")

    if len(media) == 0:
        print("[bold red]No download history to show[/bold red]")
    else:
        table = Table(show_header=True,
                      header_style="bold blue", show_lines=True)
        table.add_column("#", style="dim", width=3, justify="center")
        table.add_column("Filename", min_width=20, justify="center")
        table.add_column("Extension", min_width=20, justify="center")
        table.add_column("Resolution", min_width=15, justify="center")
        table.add_column("Link", min_width=30, justify="center")

        for idx, media in enumerate(media, start=1):
            table.add_row(str(
                idx), f'[cyan]{media.filename}[/cyan]', f'[yellow]{media.extension}[/yellow]', f'[green]{media.resolution}[/green]', f'[red]{media.link}[/red]')
        print(table)
        
@app.command(short_help="Download Youtube Video")
def video(url: str):
    return

@app.command(short_help="Download Youtube Audio")
def audio():
    return

@app.command(short_help="Download Youtube Playlist")
def playlist():
    return