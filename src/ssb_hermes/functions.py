"""Main function for adress matching.

The template and this example uses Google style docstrings as described at:
https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
"""Importing packages"""
import os
import pandas as pd
from fuzzywuzzy import process
"""Importing other internal functions"""
from ._functions import (_create_list_df_unique_value,
                        _get_value_from_df,
                        _check_all_values_equal,
                        _check_for_value,
                        _add_row,
                        _find_postnr_through_adress,
                        )

from ._find_match_rules import (
    _find_match_rule1,
    _find_match_rule2,
    _find_match_rule3,
)



def find_match(df_data: pd.DataFrame,
               df_registry: pd.DataFrame,
               *columns: str,
               registry_type_columns: str,
               find_postnr: bool = False,
               ) -> pd.DataFrame:
    """Fuction for matching adresses from data to registry.

    Args:
        df_data: Dataframe containing the data to be matched.
        df_registry: Dataframe containing the registry.
        *columns: Columns containing the data to be matched. The first column should be the group.
        registry_type_columns: Columns containing the registry type.
        find_postnr: Boolean value. If True, the function will try to find the postnr through the adress. Default is False.

    Returns:
        A dataframe containing the matched adresses.
    
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
    row_failed_adress_none = []

    for group in df_data[columns[0]].unique():
        # Subsetter ut gjeldende foretak fra vof og data inn
        df_registry_subset = df_registry.loc[df_registry[columns[0]] == group,:]
        df_data_subset = df_data.loc[df_data[columns[0]] == group,:]
        


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
                postnr_registry=postnr
            else:
                if find_postnr is True:
                    item = _find_postnr_through_adress(df_registry_subset,liste_data,postnr,columns)

                    if item != None:
                        postnr_registry = _get_value_from_df(df_registry_subset,
                            columns[1],
                            columns[2],
                            item)
                    else:
                        cant_find_postnr.append(
                                df_data_subset[df_data_subset[columns[1]] == postnr]
                            )
                        continue
                else:
                    continue
                
            liste_registry = _create_list_df_unique_value(
                    df_registry_subset,
                    columns[1],
                    columns[2],
                    postnr_registry
                )

            # Itererer gjennom hver adresse vi får inn på gitt orgnr og postnummer
            for adresse in liste_data:
                # Sjekker om det kun finnes en enhet på postnummeret i vof. Isåfall bruker jeg denne enheten
                if len(liste_registry) == 1:
                    item, rule = _find_match_rule1(liste_registry)
                # Om det fins flere enheter på samme postnr bruker jeg fuzzywuzzy for å matche dem.
                else:
                    if _check_all_values_equal(df_registry_subset,registry_type_columns):
                        score_cutoff=50
                    else:
                        score_cutoff=75
                    item, rule = _find_match_rule2(adresse, liste_registry, score_cutoff=score_cutoff)
                    # Hvis fuzzy matching ikke funker, sjekker jeg om alle enhetene har samme nace. Isåfall setter jeg bare på en enhet som ikke har None som adresse.

                    # Hvis regel 2 ikke funket, bruker jeg regel 3 til å se etter nærmeste enhet. 
                    if item is None:
                        item, rule = _find_match_rule3(df_data_subset,
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
                if rule is None:
                    row_failed_adress_none.append(_add_row(columns,
                                                           group,
                                                           adresse,
                                                           item,
                                                           postnr_registry,
                                                           postnr,
                                                           rule,
                                                           )
                                                 )

                else:
                    if postnr_registry is not None:
                        items.append(_add_row(columns,
                                              group,
                                              adresse,
                                              item,
                                              postnr_registry,
                                              postnr,
                                              rule,
                                              )
                                    )
                    else:
                        items.append(_add_row(columns,
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
    return     items, cant_find_postnr, row_failed_no_adress, row_failed_adress_none


def get_test_data():
    """Function for getting test data.

    Returns:
        Two dataframes containing test data.
    """
    data_folder = os.path.join(os.path.dirname(__file__), 'example_data')
    test_data = os.path.join(data_folder, 'test_data.csv')
    test_registry = os.path.join(data_folder, 'test_data.csv')
    
    # Read the CSV file using Pandas and return the DataFrame
    return pd.read_csv(test_data), pd.read_csv(test_registry)

