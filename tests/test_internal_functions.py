"""Script for å test funksjoner i data kategorien for transaksjonsdata"""

import os
import pandas as pd
import pytest

notebook_path = os.getcwd()
for folder_level in range(50):
    if "pyproject.toml" in os.listdir(): break
    os.chdir("../")

from src.ssb_hermes._functions import _check_for_value

data = pd.DataFrame({"col1":["hei"]})

def test__check_for_value():
    assert _check_for_value(data,"col1","hei") == True