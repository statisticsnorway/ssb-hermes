"""Main function for adress matching.

The template and this example uses Google style docstrings as described at:
https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
"""Importing packages"""
import os
from typing import Any

import pandas as pd  # type: ignore

"""Importing other internal functions"""
from ._find_match_rules import _find_match_rule1
from ._find_match_rules import _find_match_rule2
from ._find_match_rules import _find_match_rule3
from ._functions import _add_row
from ._functions import _check_all_values_equal
from ._functions import _check_for_value
from ._functions import _create_list_df_unique_value
from ._functions import _find_postnr_through_adress


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
    # Teller enheter
    i = 0
    items = []
    cant_find_postnr = []
    row_failed_no_adress = []

    for group in df_data[columns[0]].unique():
        # Subsetter ut gjeldende foretak fra vof og data inn
        df_registry_subset = df_registry.loc[df_registry[columns[0]] == group, :]
        df_data_subset = df_data.loc[df_data[columns[0]] == group, :]

        # Itererer gjennom et og et postnummer.
        for postnr in df_data_subset[columns[2]].unique():
            liste_data = None
            liste_registry = None
            postnr_registry = None

            liste_data = _create_list_df_unique_value(
                df_data_subset, columns[1], columns[2], postnr
            )

            # Sjekker om postnr finns på foretaket i vof
            if _check_for_value(df_registry_subset, columns[2], postnr):
                postnr_registry = postnr
            else:
                if find_postnr is True:
                    item = None

                    item = _find_postnr_through_adress(
                        df_registry_subset,
                        liste_data,
                        postnr,
                        columns[1],
                        columns[2],
                    )

                    if item is not None:
                        postnr_registry = item
                    else:
                        cant_find_postnr.append(
                            df_data_subset[df_data_subset[columns[1]] == postnr]
                        )
                        continue
                else:
                    continue

            liste_registry = _create_list_df_unique_value(
                df_registry_subset, columns[1], columns[2], postnr_registry
            )

            # Itererer gjennom hver adresse vi får inn på gitt orgnr og postnummer
            for adresse in liste_data:
                item = None
                # Sjekker om det kun finnes en enhet på postnummeret i vof. Isåfall bruker jeg denne enheten
                if len(liste_registry) == 1:
                    item, rule = _find_match_rule1(liste_registry)
                # Om det fins flere enheter på samme postnr bruker jeg fuzzywuzzy for å matche dem.
                else:
                    if _check_all_values_equal(
                        df_registry_subset, registry_type_columns
                    ):
                        score_cutoff = 50
                    else:
                        score_cutoff = 75
                    item, rule = _find_match_rule2(
                        adresse, liste_registry, score_cutoff=score_cutoff
                    )
                    # Hvis fuzzy matching ikke funker, sjekker jeg om alle enhetene har samme nace. Isåfall setter jeg bare på en enhet som ikke har None som adresse.

                    # Hvis regel 2 ikke funket, bruker jeg regel 3 til å se etter nærmeste enhet.
                    if item is None:
                        item, rule = _find_match_rule3(
                            df_data_subset,
                            df_registry_subset,
                            postnr,
                            adresse,
                            columns,
                        )
                        # Dersom jeg ikke finner noen match, legger jeg til enheten i en liste.
                        if item is None:
                            row_failed_no_adress.append(
                                df_data_subset[df_data_subset[columns[1]] == adresse]
                            )
                            # Hvis adressen ikke finnes fortsetter vi paa neste adresse.
                            continue

                # Store information about ident from data and registry as a dict to be made into a df.
                items.append(
                    _add_row(
                        columns,
                        group,
                        adresse,
                        item,
                        postnr_registry,
                        postnr,
                        rule,
                    )
                )

                i += 1

                if i % 1000 == 0:
                    print(f"Vi har nådd nr {i} av {len(df_data)}")

    print(f"Ferdig å kjøre {i} enhteter, fant {len(items)} enheter.")
    return items, cant_find_postnr, row_failed_no_adress


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
