"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """SSB Hermes."""


if __name__ == "__main__":
    main(prog_name="ssb-hermes")  # pragma: no cover
