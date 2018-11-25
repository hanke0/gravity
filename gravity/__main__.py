import re
from typing import TextIO, Optional

import click

from gravity import __version__


def mutually_exclusive_callback(ctx: click.Context, param: click.Option, value: Optional[str]):
    if value is not None and ctx.params.get("file"):
        raise click.UsageError("Illegal usage: yaml is mutually exclusive with file")
    return value


@click.command("gravity")
@click.option("--file", "-f", required=False, type=click.File("rt", lazy=True))
@click.argument("yaml", required=False, callback=mutually_exclusive_callback, type=click.STRING)
@click.version_option(__version__, "-v", "--version")
@click.help_option("-h", "--help")
def cli(yaml: Optional[str], file: Optional[TextIO]) -> None:
    if yaml:
        s = yaml
    elif file:
        with file as f:
            s = file.read()
    else:
        stdin = click.get_text_stream("stdin")
        s = stdin.read()
    if len(re.findall("^---$", s, re.M)) > 1:
        return run_tasks(s)
    return run_task(s)


def run_tasks(string: str):
    tasks = (i for i in re.split("^---$", string, flags=re.M) if i)
    for i in tasks:
        run_task(i)


def run_task(string: str) -> None:
    print(">>:", string[:10], sep="")


if __name__ == "__main__":
    cli()
