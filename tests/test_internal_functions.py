"""Script for å test funksjoner i data kategorien for transaksjonsdata!"""

import pandas as pd  # type: ignore

from ssb_hermes._functions import _check_for_value

data = pd.DataFrame({"col1": ["hei"]})


def test__check_for_value() -> None:
    assert _check_for_value(data, "col1", "hei") is True
