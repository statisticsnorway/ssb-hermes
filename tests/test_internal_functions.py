"""Script for å test funksjoner i data kategorien for transaksjonsdata!"""

import pandas as pd  # type: ignore

from ssb_hermes._functions import (
    _check_for_value,
    _check_all_values_equal,
    )

data = pd.DataFrame({"col1": ["hei"]})

'''Test for _check_for_value() funksjonen i _functions.py'''
def test__check_for_value() -> None:
    assert _check_for_value(data, "col1", "hei") is True

def test__check_for_value_false() -> None:
    assert _check_for_value(data, "col1", "hallo") is False

def test__check_for_value_error() -> None:
    assert _check_for_value(data, "col2", "hei") is False

'''Test for _check_all_values_equal() funksjonen i _functions.py'''
data = pd.DataFrame({"col1": ["hei", "hei"]})

data2 = pd.DataFrame({"col1": ["hei", "hallo"]})

def test__check_all_values_equal() -> None:
    assert _check_all_values_equal(data, "col1") is True

def test__check_all_values_equal_false() -> None:
    assert _check_all_values_equal(data2, "col1") is False





