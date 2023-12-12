"""Internal functions for package ssb-hermes"""

import pandas as pd
import fuzzywuzzy
from fuzzywuzzy import process

def _add_row(orgnrf,adresse,item,f_postnr,postnr,x):
    """
    Function to add dict element to list of items, can be turned into row.

    Parameters
    ----------
    orgnrf (Float): Value to check and change if true.
    adresse (str): Adress that is checked for
    item (str): Adress that is found in vof
    rule_d (int): Categorical dummy for rule 1:3, where dummy is 1:3.

    Returns
    -------
        value(str): value changed or unchanged.
    """
    item = ({'Company_Org_No':orgnrf,'Street_Address': adresse, 'vof_adress_match': item, 'f_postnr':f_postnr,'Postcode':postnr,'rule_d': x})
    return item

def _find_closest_value(df,column,value,score_cutoff: int = 40):
    """
    Function to find closest value using fuzzywuzzy.

    Parameters
    ----------
    df (pd.DataFrame): Pandas dataframe containing the data.
    column (str): String value with name of column in which to look for match.
    value (str): String value that we are looking for or equivalent off

    Returns
    -------
        item(tupple[list[str]]): Tupple with list, containing value found and percentage match.
        None: If no match
    """
    choices = df[column].to_list()
    # Har satt cutoff 40 prosent siden det er for gjort å ha 50 % feil med fire siffer
    item = process.extractOne(query=value,choices=choices,score_cutoff=score_cutoff)
    
    if item is None:
        return None, None
    else:
        return item[0], item[1]

def _check_for_value(df:pd.DataFrame,column:str,value:str) -> bool:
    """
    Function to check for value in column of df.

    Parameters
    ----------
    df (pd.DataFrame): Pandas dataframe containing the data.
    column (str): String value with name of column in which to look for value.
    value (str): String value that we are looking for.

    Returns
    -------
        bool: True if found, false if not.
    """
    if value in df[column].to_numpy():
        return True
    else:
        return False
    
def _check_all_values_equal(df,column:str):
    """
    Function to check if values in column of df are all equal.

    Parameters
    ----------
    df (pd.DataFrame): Pandas dataframe containing the data.
    column (str): String value with name of column in which to look.

    Returns
    -------
        bool: True or False.
    """
    if df[column].nunique() == 1:
        return True
    else:
        return False

def _count_items_list(items):
    """
    Function to count items in list.

    Parameters
    ----------
    items (list): List of items.

    Returns
    -------
        int: Number of items in list.
    """
    count = 0
    for item in items:
        count += 1
    return count

def _get_value_from_df(df,column1,column2,item):
    """
    Function to get value from df.

    Parameters
    ----------
    df (pd.DataFrame): Pandas dataframe containing the data.
    column1 (str): String value with name of column in which to subset rows.
    column2 (str): String value with name of column in which to look.
    item (str): String value with name of item to subset on.

    Returns
    -------
        value (str): Value from df.
    """
    value = (df[df[column1] == item].
              reset_index().
              at[0, column2]
    )
    return value

def _create_list_df_unique_value(df,column_list,column_match,value):
    """
    Function to create list from df with unique value.

    Parameters
    ----------
    df (pd.DataFrame): Pandas dataframe containing the data.
    column_list (str): String value with name of column in which to make to list.
    column_match (str): String value with name of column in which to subset rows.
    value (str): String value with name of item to subset on.

    Returns
    -------
        list_from_match (list): List with unique value.
    """
    list_from_match = (
        df.loc[
            df[column_match] == value, column_list
        ]
    ).to_list()
    return list_from_match

def _find_non_None_value(list_choices:list):
    """
    Function to find non-None value in list.

    Parameters
    ----------
    list_choices (list): List with values.

    Returns
    -------
        choice (str): Value from list.
        rule (int): Rule to be applied.
    """
    for choice in list_choices:
        if choice is not None:
            return choice
    else:
        choice=None
        return choice