import typer
from rich import print

def VerifyLink(link: str):
    if "youtu" not in link:
        print("The link entered is not a valide Youtube link")
        raise typer.Abort()
    else:
        return link