# YuDown (project under improvement)

YuDown is a python script to download YouTube video developped using [Typer](https://typer.tiangolo.com) and [Pytube](https://github.com/pytube/pytube)

## Installation

To install and run the script:

```bash
  python3 -m venv venv
  pip install yudown

  yudown --help
```

## Run Locally

To launch the project, you need [Poetry](https://python-poetry.org) to be installed

Clone the project

```bash
  git clone https://github.com/TianaNanta/yudown.git
```

Go to the project directory

```bash
  cd yudown
```

Install dependencies

```bash
  poetry install
```

Launch the project

```bash
  poetry run python -m yudown --help
```

## Usage/Examples

To download audio file from the given Youtube link

```bash
  yudown -A https://youtube.com/.....
```

## Authors

- [@TianaNanta](https://www.github.com/TianaNanta)

## License

[MIT](https://choosealicense.com/licenses/mit/)
