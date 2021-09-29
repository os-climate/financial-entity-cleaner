""" This module defines functions to validate official identifiers used in the banking industry."""

# Import python libraries here
import re

# Import third-party libraries
from stdnum import isin, lei
from stdnum.gb import sedol

# Import internal libraries
from financial_entity_cleaner import simple_cleaner


def get_ids_to_validate():
    """
    This function defines the type of patterns that can be used to name attributes related to official ids.
    The main idea is to identify automatically all the attributes in which official ids validation can be applied.

    Parameters:

    Returns:
        pattern (list): all pattern names used to identify attributes in which the id validation can be applied
    Raises:
        No exception is raised.
    """
    return ["isin", "lei", "sedol"]


def validate_id(value, type_id="isin"):
    """
    Validates an official id. By default, the id type is isin.

    Parameters:
        value (string): the id to be validated
        type_id (string): defines the type of the identifier to be validated ('lei', 'isin' or 'sedol')
    Returns:
        np.nan : if the value is not a string, is null or have zero length
        True or False: the validity of the identifier
    Raises:
        NotImplementedError: if the type_id is not recognizable
    """

    if not isinstance(value, str):
        return None

    if len(str(value).strip()) == 0:
        return None

    # Remove all unicode characters if any
    value = simple_cleaner.clean_unicode(value)

    # Remove spaces in the beginning and in the end and convert it to lower case
    value = value.strip().lower()

    # Remove excessive spaces in between words
    value = re.sub(r"\s+", " ", value)

    if type_id == "lei":
        return lei.is_valid(value)
    elif type_id == "isin":
        return isin.is_valid(value)
    elif type_id == "sedol":
        return sedol.is_valid(value)
    else:
        raise NotImplementedError
