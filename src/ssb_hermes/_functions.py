"""Internal functions for package ssb-hermes!"""

import pandas as pd
from fuzzywuzzy import process


def _add_row(
    columns: tuple,
    *args: str,
) -> dict:
    """Function to add row to dataframe.

    Args:
        columns: Tuple with column names.
        *args: Tuple with values.

    Returns:
        dict: Dictionary with values.
    """
    item = {
        columns[0]: args[0],
        f"{columns[1]}_data": args[1],
        f"{columns[1]}_registry": args[2],
        f"{columns[2]}_data": args[3],
        f"{columns[2]}_registry": args[4],
        "rule_d": args[5],
    }
    return item


def _find_closest_value(
    df: pd.DataFrame,
    column: str,
    value: str,
    score_cutoff: int = 40,
) -> tuple:
    """Function to find closest value in column of df.

    Args:
        df: Pandas dataframe containing the data.
        column: String value with name of column in which to look.
        value: String value that we are looking for.
        score_cutoff: Score cutoff. Defaults to 40.

    Returns:
        tuple: Tuple with value and score.
    """
    choices = df[column].to_list()
    # Har satt cutoff 40 prosent siden det er for gjort å ha 50 % feil med fire siffer
    item = process.extractOne(query=value, choices=choices, score_cutoff=score_cutoff)

    if item is None:
        return None, None
    else:
        return item[0], item[1]


def _check_for_value(
    df: pd.DataFrame,
    column: str,
    value: str,
) -> bool:
    """Function to check for value in column of df.

    Args:
        df: Pandas dataframe containing the data.
        column: String value with name of column in which to look.
        value: String value that we are looking for.

    Returns:
        bool: True or False.
    """
    if value in df[column].to_numpy():
        return True
    else:
        return False


def _check_all_values_equal(
    df: pd.DataFrame,
    column: str,
) -> bool:
    """Function to check if values in column of df are all equal.

    Args:
        df: Pandas dataframe containing the data.
        column: String value with name of column in which to look.

    Returns:
        bool: True or False.
    """
    if df[column].nunique() == 1:
        return True
    else:
        return False


def _get_value_from_df(
    df: pd.DataFrame,
    column1: str,
    column2: str,
    item: str,
) -> str:
    """Function to get value from df.

    Args:
        df: Pandas dataframe containing the data.
        column1: String value with name of column in which to filter rows.
        column2: String value with name of column in which to get value from.
        item: String value that we are filtering on.

    Returns:
        value: String value.
    """
    value = df[df[column1] == item].reset_index().at[0, column2]
    return value


def _create_list_df_unique_value(
    df: pd.DataFrame,
    column_list: str,
    column_match: str,
    value: str,
) -> list:
    """Function to create list from df with unique values.

    Args:
        df: Pandas dataframe containing the data.
        column_list: Column to create list from.
        column_match: String value with name of column in which to filter rows.
        value: String value that we are filtering on.

    Returns:
        list_from_match: List with values.
    """
    list_from_match = (df.loc[df[column_match] == value, column_list]).to_list()
    return list_from_match


def _set_score_cutoff(df_katalog_subset2: pd.DataFrame, column: str) -> int:
    """Function to set score cutoff.

    Args:
        df_katalog_subset2: Pandas dataframe containing the data.
        column: String value with name of column in which to look.

    Returns:
        score_cutoff: Integer value.
    """
    if _check_all_values_equal(df_katalog_subset2, column):
        score_cutoff = 0
    else:
        score_cutoff = 75
        
    return score_cutoff


def _find_postnr_through_adress(
    df_katalog_subset: pd.DataFrame,
    liste_data: list,
    postnr: str,
    columns: tuple,
) -> str:
    """Function to find postnr through adress.

    Args:
        df_katalog_subset: Pandas dataframe containing the data.
        liste_data: List with values.
        postnr: String value with postnr.
        columns: Tuple with column names.

    Returns:
        item: String value.
    """
    item = None

    for adresse in liste_data:
        item, match = _find_closest_value(
            df_katalog_subset, columns[1], adresse, score_cutoff=75
        )
        if item is None:
            continue

        else:
            # Om det finnes en match. Da stopper vi loopen og lager en liste med matchen.
            break
    else:
        # Dersom vi når enden av adresene i ibk og ikke har en match, gir vi opp og går videre til neste postnr.
        item, match = _find_closest_value(
            df_katalog_subset, columns[2], postnr, score_cutoff=50
        )

    return item
