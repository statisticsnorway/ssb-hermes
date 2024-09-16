# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
# ---

# %%
import pandas as pd

from ssb_hermes.functions import find_match
from ssb_hermes.functions import get_test_data

# %%
df_data, df_registry = get_test_data()
df_data

# %%
df_registry.at[15, "ident_postnr"] = "0388"
df_registry

# %%
items, cant_find_postnr, row_failed_no_adress = find_match(
    df_data,
    df_registry,
    "ident_gruppe",
    "ident_adresse",
    "ident_postnr",
    "ident_kommunenr",
    "ident_fylkenr",
    registry_type_columns="ident_type",
    find_postnr=True,
)

df = pd.DataFrame(items)

df
