"""Function for each rule in adress matching function.

This python file contain the three functions for adress matching based on the three rules:
    * Rule1: If there is only one unit at a location(postnr), then we use this unit.
    * Rule2: If there are multiple units we use fuzzywuzzy with 75% match.
    * Rule3: If rule 1 and 2 did not work, we iterate up geographically.
"""
"""Importing packages"""
from typing import Any

import pandas as pd  # type: ignore
from fuzzywuzzy import process  # type: ignore

"""Importing other internal functions"""
from ._functions import _check_for_value
from ._functions import _find_closest_value
from ._functions import _get_value_from_df


def _find_match_rule1(list_with_one: list[str]) -> tuple[str, int]:
    """Function for rule 1 in adress matching function. If there is only one unit at a location(postnr), then we use this unit.

    Args:
        list_with_one: List with one unit at a location(postnr).

    Returns:
        tuple: item, rule
    """
    item = list_with_one[0]
    rule = 1
    return item, rule


def _find_match_rule2(
    query: str, choices: list[str], score_cutoff: int = 75
) -> tuple[Any, Any]:
    """Function for rule 2 in adress matching function. If there are multiple units we use fuzzywuzzy with 75% match.

    Args:
        query: The query string to match.
        choices: List of choices to match against.
        score_cutoff: The score to beat in order to be considered a match.

    Returns:
        tuple: item, rule
    """
    try:
        item, match = process.extractOne(
            query=query, choices=choices, score_cutoff=score_cutoff
        )
    except (ValueError, AttributeError, TypeError):
        item = None
    finally:
        if item is None:
            rule = None
        else:
            rule = 2
    return item, rule


def _find_match_rule3(
    df_data_subset: pd.DataFrame,
    df_registry_subset: pd.DataFrame,
    postnr: str,
    adresse: str,
    columns: tuple[str, str, str, str, str],
) -> tuple[Any, Any]:
    """Function for rule 3 in adress matching function. If rule 1 and 2 did not work, we iterate up geographically.

    Args:
        df_data_subset: Subset of the data dataframe.
        df_registry_subset: Subset of the registry dataframe.
        postnr: The postnr to match against.
        adresse: The adresse to match against.
        columns: The columns to match against.

    Returns:
        tuple: item, rule
    """
    kommunenr = _get_value_from_df(df_data_subset, columns[2], columns[3], postnr)
    # kommunenr = df_data_subset[df_data_subset[columns[2]] == postnr].reset_index().at[0, columns[3]]
    fylkenr = _get_value_from_df(df_data_subset, columns[2], columns[4], postnr)
    # fylkenr = df_data_subset[df_data_subset[columns[2]] == postnr].reset_index().at[0, columns[4]]

    item = None
    rule = None

    if _check_for_value(df_registry_subset, columns[3], kommunenr):
        df_registry_subset2 = df_registry_subset.loc[
            df_registry_subset[columns[3]] == kommunenr
        ]
        item = _find_closest_value(
            df_registry_subset2, columns[1], adresse, score_cutoff=75
        )

    if item is None:
        if _check_for_value(df_registry_subset, columns[4], fylkenr):
            df_registry_subset2 = df_registry_subset.loc[
                df_registry_subset[columns[4]] == fylkenr
            ]
            item = _find_closest_value(
                df_registry_subset2, columns[1], adresse, score_cutoff=75
            )

    if item is not None:
        rule = 3

    return item, rule
