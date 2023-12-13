"""Test cases for the __main__ module."""
import sys

import pytest
from click.testing import CliRunner

sys.path.insert(0, "/ssb-hermes/src")


@pytest.fixture()
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0
