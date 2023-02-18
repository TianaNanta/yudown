from pathlib import Path

import typer
from rich import print

from yudown import audio_dir, not_spec_dir, playlist_dir, video_dir


def VerifyLink(link: str):
    if "youtu" not in link:
        print("The link entered is not a valide Youtube link")
        raise typer.Abort()
    else:
        return link
    
def validate_choice(choice: str):
    valid_choice = ["audio", "video", "playlist"]
    if choice.lower() not in valid_choice:
        raise typer.BadParameter(f"{choice} is not a valid option. Valid option are {', '.join(valid for valid in valid_choice)}")
    else:
        return choice.lower()

def validate_location(location: Path):
    if not location.is_dir():
        raise typer.BadParameter(f"The path specified {location} is not a directory")
    return location

def choise_dir(location: Path, choice: str):
    if location == not_spec_dir:
        match choice:
            case "audio":
                location = audio_dir
            case "video":
                location = video_dir
            case "playlist":
                location = playlist_dir
    return location