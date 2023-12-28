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


def _find_match_one_posible(list_with_one: list[str]) -> tuple[str, int]:
    """Function for rule 1 in adress matching function. If there is only one unit at a location(postnr), then we use this unit.

    Args:
        list_with_one: List with one unit at a location(postnr).

    Returns:
        tuple: item, rule
    """
    item = list_with_one[0]
    return item


def _find_match_fuzzy(
    query: str, choices: list[str], score_cutoff: int = 75
) -> Any:
    """Function for rule 2 in adress matching function. If there are multiple units we use fuzzywuzzy with 75% match.

    Args:
        query: The query string to match.
        choices: List of choices to match against.
        score_cutoff: The score to beat in order to be considered a match.

    Returns:
        tuple: item
    """
    try:
        item, match = process.extractOne(
            query=query, choices=choices, score_cutoff=score_cutoff
        )
    except (ValueError, AttributeError, TypeError):
        item = None
    return item
