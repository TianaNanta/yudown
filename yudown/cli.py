"""This module provides the YuDownloader CLI."""
# yudown/cli.py

import time
from typing import List, Optional

import typer
from pytube import Playlist, Search, YouTube, exceptions
from pytube.cli import on_progress
from rich import print
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn

from yudown import (__app_name__, __version__, audio_dir, not_spec_dir,
                    playlist_dir, video_dir, yudown_dir)
from yudown.database import create, destroy, read
from yudown.model import Media

app = typer.Typer(rich_markup_mode='rich')


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
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    return    


@app.command()
def download(    
    audio: Optional[bool] = typer.Option(
        False,
        "--audio",
        "-A",
        help="Download youtube Audio file",
        show_default=False
        ),
    playlist: Optional[bool] = typer.Option(
        False,
        "--playlist",
        "-P",
        help="Download youtube Playlist",
        show_default=False
        ),
    video: Optional[bool] = typer.Option(
        False,
        "--video",
        "-V",
        help="Download youtube Video file",
        show_default=False
        ),
    locate: Optional[str] = typer.Option(
        not_spec_dir,
        "--location",
        "-l",
        help="Location of the downloaded file",
        show_default=True,
    ),
    links: Optional[List[str]] = typer.Argument(None, show_default=False)
):
    if not links:
        links.append(typer.prompt("Please enter link to download"))
    
    for url in links:
        try:
			# object creation using YouTube
			# which was imported in the beginning
            yt = YouTube(url, on_progress_callback=on_progress)
            
        except exceptions.VideoPrivate:
            print("[bold red]Media is private ![/bold red]") #to handle exception
            
        except exceptions.VideoRegionBlocked:
            print("[bold red]Media is blocked ![/bold red]")
            
        except exceptions.VideoUnavailable:
            print("[bold red]Media is not available ![/bold red]")
            
        else:                
            if audio:
                fileExtension = []
                fileAudio = []
                audio = []
                
                for stream in yt.streams.order_by('mime_type').filter(type='audio'):
                    fileExtension.append(stream.mime_type)
                    fileAudio.append(stream.audio_codec)
                    audio.append(stream)

                i = 1
                
                for extension in fileExtension:
                    print(f'👉 {i}- Extension: [yellow]{extension}[/yellow] -> Audio: [bold green]{fileAudio[i-1]}[/bold green]')
                    i += 1
                    
                # To Download the video with the users Choice of resolution
                strm = int(input('\nChoose a resolution please: '))
                                
                if 1 <= strm < i:
                    try:
                        # To validate if the user enters a number displayed on the screen...
                            extension_to_download = fileExtension[strm-1]
                            print(f"You're now downloading the audio with extension {extension_to_download}...")
                            # command for downloading the video
                            file = audio[strm-1]
                            file.download(audio_dir)
                    except:
                        print("❌[bold red]Some Error, download not completed ![/bold red]❌")
                        raise typer.Abort()
                    else:
                        print("\n[bold green]Downloaded successfully ![/bold green] 🥳")
                        media = Media(filename=yt.title, extension="audio", resolution=fileExtension[strm-1], link=url)
                        create(media)
                        raise typer.Exit()
                else:
                    print("[red]Invalid choice !![/red]\n\n")
                    raise typer.Abort()
                
            elif video:
                dwn = yt.streams.filter(type="video", progressive="True", file_extension='mp4')
                print("\n👉 1- [bold green]Highest[/bold green] resolution\n👉 2- [bold red]Lowest[/bold red] resolution\n👉 3- See all available")
                res = int(input("Choose resolution: "))
                print()
    
                if res == 1:
                    try:
                        high = dwn.get_highest_resolution().resolution
                        print(f"Downloading {yt.title} [bold italic green]{high}[/bold italic green]")
                        dwn.get_highest_resolution().download(video_dir, filename=yt.title+"_"+high)
                    except:
                        print(f"Error while downloading the video !")
                        raise typer.Abort()
                    else:
                        print("\nDownload success !!")
                        video1 = Media(filename=yt.title, extension="mp4", resolution=high, link=url)
                        create(video1)
                        raise typer.Exit()
                    
                elif res == 2:
                    try:
                        low = dwn.get_lowest_resolution().resolution
                        print(f"Downloading {yt.title} [bold italic red]{low}[/bold italic red]")
                        dwn.get_lowest_resolution().download(video_dir, filename=yt.title+"_"+low)
                    except:
                        print(f"Error while downloading the video !")
                        raise typer.Abort()
                    else:
                        print("\nDownload success !!")
                        video2 = Media(filename=yt.title, extension="mp4", resolution=low, link=url)
                        create(video2)
                        raise typer.Exit()

                elif res == 3:        
                    video_resolutions = []
                    fileExtension = []
                    videos = []
		
                    for stream in yt.streams.order_by('resolution').filter(progressive="True"):
                        video_resolutions.append(stream.resolution)
                        fileExtension.append(stream.mime_type)
                        videos.append(stream)
		
                    i = 1
                    for resolution in video_resolutions:
                        print(f'👉 {i}- [green]{resolution}[/green] -> Extension: {fileExtension[i-1]}')
                        i += 1

					# To Download the video with the users Choice of resolution
                    strm = int(input('\nChoose a resolution please: '))
					
                    if 1 <= strm < i:
                        try:
							# To validate if the user enters a number displayed on the screen...
                            resolution_to_download = video_resolutions[strm-1]
                            print(f"You're now downloading the video with resolution [bold italic green]{resolution_to_download}[/bold italic green]...")

								# command for downloading the video
                            videos[strm-1].download(video_dir, filename=yt.title+"_"+resolution_to_download)
                        except:
                            print("[bold red]Some Error, download not completed ![/bold red]")
                            raise typer.Abort()
                        else:
                            print("\nDownloaded successfully !")
                            video3 = Media(filename=yt.title, extension="mp4", resolution=resolution_to_download, link=url)
                            create(video3)
                            raise typer.Exit()
                    else:
                        print("Invalid choice !!\n\n")
                        raise typer.Abort()
 
                else:
                    print("Error ! Enter a valid number !!")
                    raise typer.Abort()
                
            elif playlist:
                pass
            else:
                print(f"Link: {url}")


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
        table.add_column("Extension", min_width=20, justify="center")
        table.add_column("Resolution", min_width=15, justify="center")
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
    table.add_column("Title", min_width=30, justify="center")
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