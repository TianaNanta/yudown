"""This module provides the YuDownloader CLI."""
# yudown/cli.py

import time
from pathlib import Path
from typing import List, Optional

import typer
from pytube import Search, YouTube, exceptions
from pytube.cli import on_progress
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich.table import Table

from yudown import __app_name__, __version__, not_spec_dir, playlist_dir
from yudown.database import create, destroy, read
from yudown.model import Media
from yudown.playlist import PlaylistObject
from yudown.utils import (VerifyLink, choise_dir, validate_choice,
                          validate_location)

app = typer.Typer(rich_markup_mode='rich')


def _version_callback(value: bool) -> None:
    if value:
        print(f"[bold red]{__app_name__}[/bold red] [green]v{__version__}[/green]")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    return


@app.command()
def history(
    clear: Optional[bool] = typer.Option(
        None,
        "--delete",
        "-D",
        show_default=False,
    )
    ):
    """ Show the download [blue]history[/blue] ⌚️"""
    
    if clear:
        delete = typer.confirm("Are you sure to clear all history ?", abort=True)
        if delete:
            print("History deleted")
            destroy()
            raise typer.Exit()
            
    media = read()

    print("📜", "[bold magenta]Download History[/bold magenta]", "📜")

    if len(media) == 0:
        print("[bold red]No download history to show[/bold red]")
    else:
        table = Table(show_header=True,
                      header_style="bold", show_lines=True)
        table.add_column("#", style="dim", width=3, justify="center")
        table.add_column("Filename", min_width=20, justify="center")
        table.add_column("Extension", min_width=3, justify="center")
        table.add_column("Resolution", min_width=5, justify="center")
        table.add_column("Link", min_width=30, justify="center")

        for idx, media in enumerate(media, start=1):
            table.add_row(
                str(idx), f'[cyan]{media.filename}[/cyan]', f'[yellow]{media.extension}[/yellow]', f'[green]{media.resolution}[/green]', f'[red]{media.link}[/red]')
        print(table)
        
        
@app.command("search")
def make_search(
    search_query: Optional[str] = typer.Argument("", help="The word you are searching for", show_default=False),
    suggestion: Optional[bool] = typer.Option(
        None,
        "--suggestion",
        "-s",
        help="Show search suggestion",
        show_default=False
    )
    ):
    """[blue]Search[/blue] for video on Youtube 🔍"""
    
    if search_query == "":
        search_query = Prompt.ask("Enter a word to search for: ")
    
    s = Search(search_query)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=False,
    ) as progress:
        progress.add_task(description="Searching...", total=None)
        time.sleep(60)
    
    table = Table(
        show_header=True,
        header_style="bold",
        show_lines=True
    )
    table.add_column("#", style="dim", width=3, justify="center")
    table.add_column("Title", min_width=20, justify="center")
    table.add_column("Link", min_width=20, justify="center")
    
    resultat = s.results
    for idx, resultat in enumerate(resultat, start=1):
        table.add_row(
                str(idx), f'[cyan]{resultat.title}[/cyan]', f'[yellow]{resultat.watch_url}[/yellow]')
    print(table)
    
    if suggestion:
        for i in s.completion_suggestions:
            print(f"{i}")
        print(f"[bold green]{len(s.completion_suggestions)}[/bold green] suggestions founded\n")
    
    raise typer.Exit()


@app.command("playlist")
def PlaylistDownload(
    link: Optional[str] = typer.Argument(
        None,
        show_default=False
    ),
    locate: Optional[Path] = typer.Option(
        playlist_dir,
        "--location",
        "-l",
        help="Location of the files to download",
        show_default=True
    )
):
    """Download Youtube [yellow]Playlist[/yellow] video 📼"""
    if link == None:
        #link of the video to be downloader
        link = input("Enter the playlist link")
    
    url = VerifyLink(link)
    playlist = PlaylistObject(url)
    
    try:
        for video in playlist.videos:
            table = Table(
                show_header=True,
                header_style="bold",
                show_lines=True
            )
            table.add_column("#", style="dim", width=3, justify="center")
            table.add_column("Title", min_width=20, justify="center")
            table.add_column("Link", min_width=20, justify="center")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=False,
            ) as progress:
                progress.add_task(description="Fetching...", total=None)
                time.sleep(30)
            
            for idx, video in enumerate(video, start=1):
                table.add_row(
                        str(idx), f'[cyan]{video.title}[/cyan]', f'[yellow]{video.watch_url}[/yellow]')
            print(table)
            
            down = typer.confirm("Download this playlist ?")
            if not down:
                raise typer.Abort()
            print(f"Downloading {playlist.title}")
            video.streams.first().download(locate)
    except:
        print("Some error, download not completed !")
        raise typer.Abort()
    else:
        play = Media(filename=video.title, extension="mp4", resolution="Playlist", link=video.watch_url)
        create(play)
        
        print("Downloaded successfully !")
        raise typer.Exit()


@app.command()
def download(    
    type: Optional[str] = typer.Option(
        "video",
        "--type",
        "-t",
        help="The type of media to download",
        show_default=True,
        callback=validate_choice,
    ),
    location: Optional[Path] = typer.Option(
        not_spec_dir,
        "--location",
        "-l",
        help="Location of the downloaded file",
        show_default=True,
        callback=validate_location,
    ),
    links: Optional[List[str]] = typer.Argument(None, show_default=False)
):
    """Download file from [red]Youtube[/red] 📥"""
    if not links:
        links.append(VerifyLink(input("Please enter link to download")))
    
    for url in links:
        try:
			# object creation using YouTube
			# which was imported in the beginning
            link = VerifyLink(url)
            yt = YouTube(link, on_progress_callback=on_progress)
            title = yt.title
            
        except exceptions.VideoPrivate:
            print("[bold red]Media is private ![/bold red]") #to handle exception
            
        except exceptions.VideoRegionBlocked:
            print("[bold red]Media is blocked ![/bold red]")
            
        except exceptions.VideoUnavailable:
            print("[bold red]Media is not available ![/bold red]")
            
        else:
            match type:
                case "audio":
                    audiobj = yt.streams.order_by('mime_type').filter(type='audio')

                    fileExtension = [stream.mime_type for stream in audiobj]
                    audio = [stream for stream in audiobj]
                    
                    locate = choise_dir(location, "audio")

                    i = 1
                    
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        transient=False,
                    ) as progress:
                        progress.add_task(description="Fetching...", total=None)
                        time.sleep(30)
                    
                    table = Table(
                        show_header=True,
                        header_style="bold",
                        show_lines=True
                    )
                    table.add_column("#", style="dim", width=3, justify="center")
                    table.add_column("Title", min_width=20, justify="center")
                    table.add_column("Type", min_width=3, justify="center")
                    table.add_column("Extension", min_width=3, justify="center")
                    
                    for stream in audiobj:
                        table.add_row(
                        str(i), f'[cyan]{title}[/cyan]', f'[yellow]{stream.audio_codec}[/yellow]', f'[green]{stream.mime_type}[/green]')
                        i += 1
                    print(table)
                        
                    # To Download the video with the users Choice of resolution
                    strm = int(input('\nChoose a resolution please: '))
                                    
                    if 1 <= strm < i:
                        try:
                            # To validate if the user enters a number displayed on the screen...
                                extension_to_download = fileExtension[strm-1]
                                
                                down = typer.confirm(f"Confirm downloading {title} {extension_to_download} ?")                                
                                if not down:
                                    raise typer.Abort()
                                # command for downloading the video
                                print(f"You're now downloading the audio with extension {extension_to_download}...")
                                file = audio[strm-1]
                                file.download(locate)
                        except:
                            print("❌[bold red]Some Error, download not completed ![/bold red]❌")
                            raise typer.Abort()
                        else:
                            print("\n[bold green]Downloaded successfully ![/bold green] 🥳")
                            media = Media(filename=title, extension="audio", resolution=fileExtension[strm-1], link=url)
                            create(media)
                            raise typer.Exit()
                    else:
                        print("[red]Invalid choice !![/red]\n\n")
                        raise typer.Abort()
                
                case "video":                    
                    locate = choise_dir(location, "video")
                    dwn = yt.streams.filter(type="video", progressive="True", file_extension='mp4')
                    print("\n👉 1- [bold green]Highest[/bold green] resolution\n👉 2- [bold red]Lowest[/bold red] resolution\n👉 3- See all available")
                    res = int(input("Choose resolution: "))
                    print()
        
                    if res == 1:
                        try:
                            high = dwn.get_highest_resolution().resolution
                            
                            print(f"Downloading {title} [bold italic green]{high}[/bold italic green]")
                            
                            dwn.get_highest_resolution().download(locate, filename=title+" "+high)
                        except:
                            print(f"Error while downloading the video !")
                            raise typer.Abort()
                        else:
                            print("\nDownload success !!")
                            video1 = Media(filename=title, extension="mp4", resolution=high, link=url)
                            create(video1)
                            raise typer.Exit()
                        
                    elif res == 2:
                        try:
                            low = dwn.get_lowest_resolution().resolution
                            
                            print(f"Downloading {title} [bold italic red]{low}[/bold italic red]")
                            
                            dwn.get_lowest_resolution().download(locate, filename=title+" "+low)
                        except:
                            print(f"Error while downloading the video !")
                            raise typer.Abort()
                        else:
                            print("\nDownload success !!")
                            video2 = Media(filename=title, extension="mp4", resolution=low, link=url)
                            create(video2)
                            raise typer.Exit()

                    elif res == 3:
                        videobj = yt.streams.order_by('resolution').filter(progressive="True")
                        
                        video_resolutions = [stream.resolution for stream in videobj]
                        fileExtension = [stream.mime_type for stream in videobj]
                        videos = [stream for stream in videobj]		
                        i = 1
                        
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[progress.description]{task.description}"),
                            transient=False,
                        ) as progress:
                            progress.add_task(description="Fetching...", total=None)
                            time.sleep(30)
                        
                        table = Table(
                            show_header=True,
                            header_style="bold",
                            show_lines=True
                        )
                        table.add_column("#", style="dim", width=3, justify="center")
                        table.add_column("Title", min_width=20, justify="center")
                        table.add_column("Resolution", min_width=3, justify="center")
                        table.add_column("Extension", min_width=5, justify="center")
                        
                        for stream in videobj:
                            table.add_row(
                            str(i), f'[cyan]{title}[/cyan]', f'[yellow]{stream.resolution}[/yellow]', f'[green]{stream.mime_type}[/green]')
                            i += 1
                        print(table)

                        # To Download the video with the users Choice of resolution
                        strm = int(input('\nChoose a resolution please: '))
                        
                        if 1 <= strm < i:
                            try:
                                # To validate if the user enters a number displayed on the screen...
                                resolution_to_download = video_resolutions[strm-1]
                                
                                downl = typer.confirm(f"Confirm downloading {title} {resolution_to_download} ?")
                                if not downl:
                                    raise typer.Abort()
                                print(f"You're now downloading the video with resolution [bold italic green]{resolution_to_download}[/bold italic green]...")

                                videos[strm-1].download(locate, filename=title+" "+resolution_to_download)
                                
                            except:
                                print("[bold red]Some Error, download not completed ![/bold red]")
                                raise typer.Abort()
                            else:
                                print("\nDownloaded successfully !")
                                video3 = Media(filename=title, extension="mp4", resolution=resolution_to_download, link=url)
                                create(video3)
                                raise typer.Exit()
                        else:
                            print("Invalid choice !!\n\n")
                            raise typer.Abort()
    
                    else:
                        print("Error ! Enter a valid number !!")
                        raise typer.Abort()
                case "playlist":
                    locate = choise_dir(location, "playlist")
                    for i in links:
                        PlaylistDownload(i, locate)