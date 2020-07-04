# -*- coding: utf-8 -*-

"""Console script for auto_py2to3."""
import sys
import click


@click.command()
def main():
    """Console script for auto_py2to3."""
    click.echo("Replace this message by putting your code into "
               "auto_py2to3.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
