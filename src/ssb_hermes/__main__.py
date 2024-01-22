"""Command-line interface."""
.functions import find_match

@click.command()
@click.version_option()
def main() -> None:
    """SSB Hermes."""
    find_match()



if __name__ == "__main__":
    main(prog_name="ssb_hermes")  # pragma: no cover
