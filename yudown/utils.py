import typer
from rich import print

def VerifyLink(link: str):
    if "youtu" not in link:
        print("The link entered is not a valide Youtube link")
        raise typer.Abort()
    else:
        return link
    
def validate_choice(choice: str):
    valid_choice = ["audio", "video", "playlist"]
    if choice.lower() not in valid_choice:
        raise typer.BadParameter(f"{choice} is not a valid option. Valid option are {f', '.join(valid for valid in valid_choice)}")
    else:
        return choice.lower()