# -*- coding: UTF-8 -*-
import typer

from cli import app


def main():
    try:
        app(prog_name='blog')
    except KeyboardInterrupt:
        raise typer.Exit()


if __name__ == "__main__":
    main()
