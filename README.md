# `YuDown`

Download Youtube Media from this script and have a wonderful output😋

## Installation

To install and run the script:

```console
  python3 -m venv venv
  pip install yudown

  yudown --help
```

## Run Locally

To launch the project, you need [Poetry](https://python-poetry.org) to be installed

Clone the project

```console
  git clone https://github.com/TianaNanta/yudown.git
```

Go to the project directory

```console
  cd yudown
```

Install dependencies

```console
  poetry install
```

Launch the project

```console
  poetry run python -m yudown --help
```

## Usage

**Usage**:

```console
yudown [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-v, --version`: Show the application's version and exit.
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `download`: Download file from [red]Youtube[/red] 📥
* `history`: Show the download [blue]history[/blue] ⌚️
* `playlist`: Download Youtube [yellow]Playlist[/yellow]...
* `search`: [blue]Search[/blue] for video on Youtube 🔍

## `yudown download`

Download file from [red]Youtube[/red] 📥

**Usage**:

```console
yudown download [OPTIONS] [LINKS]...
```

**Arguments**:

* `[LINKS]...`

**Options**:

* `-t, --type TEXT`: The type of media to download  [default: video]
* `-l, --location PATH`: Location of the downloaded file  [default: ~/YuDown/notSpecified]
* `--help`: Show this message and exit.

## `yudown history`

Show the download [blue]history[/blue] ⌚️

**Usage**:

```console
yudown history [OPTIONS]
```

**Options**:

* `-D, --delete`
* `--help`: Show this message and exit.

## `yudown playlist`

Download Youtube [yellow]Playlist[/yellow] video 📼

**Usage**:

```console
yudown playlist [OPTIONS] [LINK]
```

**Arguments**:

* `[LINK]`

**Options**:

* `-l, --location PATH`: Location of the files to download  [default: /home/nanta/YuDown/Playlist]
* `--help`: Show this message and exit.

## `yudown search`

[blue]Search[/blue] for video on Youtube 🔍

**Usage**:

```console
yudown search [OPTIONS] [SEARCH_QUERY]
```

**Arguments**:

* `[SEARCH_QUERY]`: The word you are searching for

**Options**:

* `-s, --suggestion`: Show search suggestion
* `--help`: Show this message and exit.

## Authors

* [@TianaNanta](https://www.github.com/TianaNanta)

## License

[MIT](https://choosealicense.com/licenses/mit/)
