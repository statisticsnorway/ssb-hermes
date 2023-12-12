"""A collection of useful functions.

The template and this example uses Google style docstrings as described at:
https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
"""Importing packages"""
import pandas as pd
from fuzzywuzzy import process
"""Importing other internal functions"""
from _functions import *

def _find_match_rule1(list_with_one):
    """
    Function to return item and rule if list contains only one item.

    Parameters
    ----------
    list_with_one (list): List with one item.

    Returns
    -------
        item (list): List with one item.
        rule (int): Rule to be applied.
    """
    item = list_with_one[0]
    rule = 1
    return item, rule


def _find_match_rule2(query, choices, score_cutoff: int = 75):
    try:
        item, match = process.extractOne(
            query=query, choices=choices, score_cutoff=score_cutoff
        )
    except:
        item = None
    finally:
        if item is None:
            rule = None
        else:
            rule = 2
    return item, rule


def _find_match_rule3(choices, df, column):
    if _check_all_values_equal(
        df,
        column,
    ):
        item = _find_non_None_value(choices)
        rule = 3
    else:
        item = None
        rule = None
    return item, rule




def _find_match_rule4(df_data_subset,df_katalog_subset,postnr,adresse):
    kommunenr = df_data_subset[df_data_subset["Postcode"] == postnr].reset_index().at[0, "kommunenr"]
    fylkenr = df_data_subset[df_data_subset["Postcode"] == postnr].reset_index().at[0, "fylkenr"]
    if check_for_value(df_katalog_subset, "kommunenr", kommunenr):
        df_katalog_subset2 = df_katalog_subset[df_katalog_subset["kommunenr"] == kommunenr]
        if check_all_values_equal(df_katalog_subset2, "nace1_sn07"):
            score_cutoff = 0
        else:
            score_cutoff = 75

        item, match = find_closest_value(df_katalog_subset2, "f_adr1", adresse, score_cutoff=score_cutoff)
        
        if item is None:
            rule = None
        else:
            rule = 4
    elif check_for_value(df_katalog_subset, "fylkenr", fylkenr):
        df_katalog_subset2 = df_katalog_subset[df_katalog_subset["fylkenr"] == fylkenr]
        if check_all_values_equal(df_katalog_subset2, "nace1_sn07"):
            score_cutoff = 0
        else:
            score_cutoff = 75

        item, match = find_closest_value(df_katalog_subset2, "f_adr1", adresse, score_cutoff=score_cutoff)
        if item is None:
            rule = None
        else:
            rule = 4
    else:
        item = None
        rule = None
        
    return item, rule


def find_match(df_data,df_katalog):
    # Teller enheter
    i = 0
    items = []
    cant_find_postnr = []
    row_failed_no_adress = []
    row_failed_adress_none = []

    for orgnr in df_data["Company_Org_No"].unique():
        # Subsetter ut gjeldende foretak fra vof og data inn
        df_katalog_subset = df_katalog[df_katalog["org_nr"] == orgnr]
        df_data_subset = df_data[df_data["Company_Org_No"] == orgnr]
        


        # Itererer gjennom et og et postnummer.
        for postnr in df_data_subset["Postcode"].unique():
            liste_ibk = None
            liste_vof = None
            #Setter postnr_vof som None for å evt sette inn verdi
            postnr_vof = None
            liste_ibk = create_list_df_unique_value(
                df_data_subset, "Street_Address", "Postcode", postnr
            )

            # Sjekker om postnr finns på foretaket i vof
            if check_for_value(df_katalog_subset, "f_postnr", postnr):
                liste_vof = create_list_df_unique_value(
                    df_katalog_subset, "f_adr1", "f_postnr", postnr
                )

            else:
                # Dersom ingen postnummer ligner sjekker jeg at ingen adresse ligner.
                for adresse in liste_ibk:
                    item, match = find_closest_value(
                        df_katalog_subset, "f_adr1", adresse, score_cutoff=75
                    )
                    if item is None:
                        continue

                    else:
                        postnr_vof = get_value_from_df(
                            df_katalog_subset, "f_adr1", "f_postnr", item
                        )
                        liste_vof = create_list_df_unique_value(
                            df_katalog_subset, "f_adr1", "f_postnr", postnr_vof
                        )
                        #Om det finnes en match. Da stopper vi loopen og lager en liste med matchen.
                        break
                else:
                    #Dersom vi når enden av adresene i ibk og ikke har en match, gir vi opp og går videre til neste postnr.
                    item, match = find_closest_value(
                        df_katalog_subset, "f_postnr", postnr, score_cutoff=50
                    )

                    if item is None:
                        cant_find_postnr.append(
                            df_data_subset[df_data_subset["Postcode"] == postnr]
                        )
                        continue
                    else:
                        postnr_vof = item
                        liste_vof = create_list_df_unique_value(
                            df_katalog_subset, "f_adr1", "f_postnr", postnr_vof
                        )
            # Itererer gjennom hver adresse vi får inn på gitt orgnr og postnummer
            for adresse in liste_ibk:
                # Sjekker om det kun finnes en enhet på postnummeret i vof. Isåfall bruker jeg denne enheten
                if count_items_list(liste_vof) == 1:
                    item, rule = _find_match_rule1(liste_vof)
                # Om det fins flere enheter på samme postnr bruker jeg fuzzywuzzy for å matche dem.
                else:
                    item, rule = _find_match_rule2(adresse, liste_vof, score_cutoff=75)
                    # Hvis fuzzy matching ikke funker, sjekker jeg om alle enhetene har samme nace. Isåfall setter jeg bare på en enhet som ikke har None som adresse.
                    if item is None:
                        item, rule = _find_match_rule3(
                            liste_vof,
                            df_katalog_subset[df_katalog_subset["f_postnr"] == postnr],
                            "nace1_sn07"
                        )
                        # Hvis regel 3 funket, bruker jeg regel 4 til å se etter nærmeste enhet. 
                        if item is None:
                            item, rule = _find_match_rule4(df_data_subset,
                                                            df_katalog_subset,
                                                            postnr,
                                                            adresse
                                                        )
                            # Dersom jeg ikke finner noen match, legger jeg til enheten i en liste.
                            if item is None:
                                row_failed_no_adress.append(
                                    df_data_subset[df_data_subset["Street_Address"] == adresse]
                                )
                if rule is None:
                    row_failed_adress_none.append(add_row(orgnr, adresse, item, postnr,postnr, rule))

                else:
                    if postnr_vof is not None:
                        items.append(add_row(orgnr, adresse, item, postnr_vof, postnr, rule))
                    else:
                        items.append(add_row(orgnr, adresse, item, postnr, postnr, rule))

                i += 1

                if i % 1000 == 0:
                    print(f"Vi har nådd nr {i} av {len(df_data)}")

    print(f"Ferdig å kjøre {i} enhteter, fant {len(items)} enheter.")
    return     items, cant_find_postnr, row_failed_no_adress,row_failed_adress_none
