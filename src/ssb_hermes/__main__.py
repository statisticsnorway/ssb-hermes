"""Command-line interface."""
import click

from .functions import _find_match_rule1
from .functions import _find_match_rule2
from .functions import _find_match_rule3
from .functions import _find_match_rule4


@click.command()
@click.version_option()
def main() -> None:
    """SSB Hermes."""

if __name__ == "__main__":
    adresse_matching(prog_name="ssb-hermes")  # pragma: no cover
