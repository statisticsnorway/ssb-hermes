"""Main function for adress matching.

The template and this example uses Google style docstrings as described at:
https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
"""Importing packages"""
import os
from typing import Any

import pandas as pd  # type: ignore

"""Importing other internal functions"""
from ._find_match_rules import _find_match_one_posible
from ._find_match_rules import _find_match_fuzzy
from ._functions import _add_row
from ._functions import _check_all_values_equal
from ._functions import _check_for_value
from ._functions import _create_list_df_unique_value
from ._functions import _find_postnr_through_adress

def get_test_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Function for getting test data.

    Returns:
        tuple:Two dataframes containing test data.
    """
    data_folder = os.path.join(os.path.dirname(__file__), "example_data")
    test_data = os.path.join(data_folder, "test_data.csv")
    test_registry = os.path.join(data_folder, "test_data.csv")

    # Read the CSV file using Pandas and return the DataFrame
    df1 = pd.read_csv(
        test_data,
        header=0,
        names=[
            "ident_gruppe",
            "ident_type",
            "ident_adresse",
            "ident_postnr",
            "ident_kommunenr",
            "ident_fylkenr",
        ],
        dtype={
            "ident_gruppe": str,
            "ident_type": str,
            "ident_adresse": str,
            "ident_postnr": str,
            "ident_kommunenr": str,
            "ident_fylkenr": str,
        },
    )
    df2 = pd.read_csv(
        test_registry,
        header=0,
        names=[
            "ident_gruppe",
            "ident_type",
            "ident_adresse",
            "ident_postnr",
            "ident_kommunenr",
            "ident_fylkenr",
        ],
        dtype={
            "ident_gruppe": str,
            "ident_type": str,
            "ident_adresse": str,
            "ident_postnr": str,
            "ident_kommunenr": str,
            "ident_fylkenr": str,
        },
    )
    return df1, df2

    


def _find_match_one_posible(list_with_one: list[str]) -> tuple[str, int]:
    """Function for rule 1 in adress matching function. If there is only one unit at a location(postnr), then we use this unit.

    Args:
        list_with_one: List with one unit at a location(postnr).

    Returns:
        tuple: item, rule
    """
    item = list_with_one[0]
    rule = 1
    return item, rule


def _find_match_fuzzy(
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

def find_match(
    df_data: pd.DataFrame,
    df_registry: pd.DataFrame,
    *columns: str,
    registry_type_columns: str,
    find_postnr: bool = False,
) -> tuple[Any, Any, Any]:
    """Fuction for matching adresses from data to registry.

    Args:
        df_data: Dataframe containing the data to be matched.
        df_registry: Dataframe containing the registry.
        *columns: Columns containing the data to be matched. The first column should be the group.
        registry_type_columns: Columns containing the registry type.
        find_postnr: Boolean value. If True, the function will try to find the postnr through the adress. Default is False.

    Returns:
        tuple: A tuple containing rows to make the matched df from, filtered df with wrong postid, filtered df with fauilty adresses.

    Raises:
        ValueError: If the number of columns is not 5.
    """
    if len(columns) != 5:
        raise ValueError("Exactly five columns are required.")
    # Counter for units
    i = 0
    # List for storing matched units
    items = []
    # List for storing units where we could not find.
    no_match = []

    for group in df_data[columns[0]].unique():
        # Subsetting out group from data and registry
        df_registry_subset = df_registry.loc[df_registry[columns[0]] == group, :]
        df_data_subset = df_data.loc[df_data[columns[0]] == group, :]

        # Making list for country
        list_country = df_registry_subset[columns[1]].unique().list()

        # Setting score_cutoff for fuzzywuzzy
        if _check_all_values_equal(
                df_registry_subset, registry_type_columns
            ):
            score_cutoff = 50
        else:
            score_cutoff = 75

        # Iterating through each postnr
        for postnr in df_data_subset[columns[2]].unique():
            # Getting kommunenr and fylkenr from data
            kommune = df_data_subset.loc[df_data_subset[columns[2]] == postnr, columns[4]].unique()[0]
            fylke = df_data_subset.loc[df_data_subset[columns[2]] == postnr, columns[5]].unique()[0]

            # Subsetting out postnr from data
            df_data_subset_postnr = df_data_subset.loc[df_data_subset[columns[2]] == postnr, :]

            # Making list of adresses for each geographical level.
            list_postnr = df_registry_subset.loc[df_registry_subset[columns[2]] == postnr, columns[1]].list()
            list_kommune = df_registry_subset.loc[df_registry_subset[columns[4]] == kommune, columns[1]].list()
            list_fylke = df_registry_subset.loc[df_registry_subset[columns[5]] == fylke, columns[1]].list()

            # Iterating through each adresse in postnr
            for adresse in df_data_subset_postnr[columns[1]].unique():
                item = None
                # Checking if there is only one unit in the postnr in the registry. If so, using this unit.
                if len(list_postnr) == 1:
                    item, rule = _find_match_one_posible(list_postnr)
                    rule = 1
                # If there are more than one unit in the postnr, using fuzzywuzzy to match them.
                # We check on each geographical level from lowest to highest.
                if item is None:
                    item, rule = _find_match_fuzzy(
                        adresse, list_postnr, score_cutoff=score_cutoff
                    )
                    rule = 2
                
                if item is None:
                    item, rule = _find_match_fuzzy(
                        adresse, list_kommune, score_cutoff=score_cutoff
                    )
                    rule = 3
                
                if item is None:
                    item, rule = _find_match_fuzzy(
                        adresse, list_fylke, score_cutoff=score_cutoff
                    )
                    rule = 4
                
                if item is None:
                    item, rule = _find_match_fuzzy(
                        adresse, list_country, score_cutoff=score_cutoff
                    )
                    rule = 5
                
                # If fuzzy matching does not work, we check if all units have the same nace.
                # If so, we use the best matching adress in the country.
                if item is None:
                    if _check_all_values_equal(
                        df_registry_subset, registry_type_columns
                    ):
                        score_cutoff = 0
                        item, rule = _find_match_fuzzy(
                            list_country, score_cutoff=score_cutoff
                        )
                        rule = 6
                
                if item is None:
                    no_match.append(
                        df_data_subset_postnr[df_data_subset_postnr[columns[1]] == adresse]
                    )
                else:

                    items.append(
                        _add_row(
                            columns,
                            group,
                            adresse,
                            item,
                            postnr,
                            postnr,
                            rule,
                        )
                    )
                
                i += 1

                if i % 1000 == 0:
                    print(f"Vi har nådd nr {i} av {len(df_data)}")

    print(f"Ferdig å kjøre {i} enhteter, fant {len(items)} enheter.")
    return items, no_match     