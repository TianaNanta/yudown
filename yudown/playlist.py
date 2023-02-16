from typing import Optional

import typer
from pytube import Playlist, exceptions
from rich import print


def PlaylistObject(link: Optional[str]):    
    try:
        # object creating using Youtube
        pylst = Playlist(link)
    except exceptions.VideoPrivate:
        print("[bold red]Media is private ![/bold red]")
        raise typer.Abort()
    except exceptions.VideoRegionBlocked:
        print("[bold red]Media is blocked ![/bold red]")
        raise typer.Abort()
    except exceptions.VideoUnavailable:
        print("[bold red]Media is not available ![/bold red]")
        raise typer.Abort()
    else:
        return pylst