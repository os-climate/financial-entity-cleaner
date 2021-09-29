""" This module defines functions to normalize country information based on the database available in
    the hdx-python-country API"""

# Import python libraries
import numpy as np
import re

# Import third-party libraries
from hdx.location.country import Country

# Import internal libraries
from financial_entity_cleaner import simple_cleaner


def get_pattern_country_to_clean():
    """
    This function defines the type of patterns that can be used to name attributes related to country info.
    The main idea is to identify automatically all the attributes in which country validation can be applied.

    Parameters:

    Returns:
        pattern (list): all pattern names used to identify attributes in which the cleaning can be applied
    Raises:
        No exception is raised.
    """
    return ["country", "country_name", "alpha2", "alpha3"]


def get_country_info(country, output_lettercase="lower"):
    """
    This function defines the type of patterns that can be used to name attributes related to country info.
    The main idea is to identify automatically all the attributes in which country validation can be applied.

    Parameters:
        country (string): a string with country info (name or alpha codes)
        output_lettercase (string): indicates the letter case (lower, by default) as the result of the cleaning

    Returns:
        dict_country (dictionary): return a dictionary of country info or None
            - dictionary: containing the name, alpha2 and alpha3 code if the country informed is valid
            - None: if the country informed couldn't be found, is not a string or is invalid due to its size
    Raises:
        No exception is raised.
    """
    if not isinstance(country, str):
        return None

    if len(str(country).strip()) < 2:
        return None

    # Remove all unicode characters if any
    value = simple_cleaner.clean_unicode(country)

    # Remove spaces in the beginning and in the end and convert it to lower case
    value = value.strip().lower()

    # Remove excessive spaces in between words
    value = re.sub(r"\s+", " ", value)

    dict_country = {}
    country_name = np.nan
    alpha2_name = np.nan
    alpha3_name = np.nan

    if len(value) == 2:
        country_name = get_name_from_alpha2(value)
        if country_name:
            alpha2_name = value
            alpha3_name = get_alpha3_from_name(country_name)
    elif len(value) == 3:
        country_name = get_name_from_alpha3(value)
        if country_name:
            alpha3_name = value
            alpha2_name = get_alpha2_from_alpha3(alpha3_name)
    else:
        alpha3_name = get_alpha3_from_name(value)
        if alpha3_name:
            alpha3_name = alpha3_name
            country_name = get_name_from_alpha3(alpha3_name)
            alpha2_name = get_alpha2_from_alpha3(alpha3_name)

    if country_name and alpha2_name and alpha3_name:
        # Get the dictionary with all information about the country
        dict_country["country_name"] = country_name
        dict_country["country_alpha2"] = alpha2_name
        dict_country["country_alpha3"] = alpha3_name

        # Apply the requested letter case
        # By default the function returns the result in lower case
        for key in dict_country.keys():
            if output_lettercase == "upper":
                dict_country[key] = dict_country[key].upper()
            elif output_lettercase == "lower":
                dict_country[key] = dict_country[key].lower()
            elif output_lettercase == "title":
                dict_country[key] = dict_country[key].title()
        return dict_country
    else:
        return None


def get_name_from_alpha2(country):
    """
    Gets the name of a country given its alpha2 code.

    Parameters:
        country (string): the alpha2 code
    Returns:
        NaN (np.nan): if the alpha code was not found
        country_name (string): the name of the country
    Raises:
        No exception is raised.
    """

    country_name = Country.get_country_name_from_iso2(country, use_live=False)
    if not country_name:
        return None
    return country_name


def get_name_from_alpha3(country):
    """
    Gets the name of a country given its alpha3 code.

    Parameters:
        country (string): the alpha3 code
    Returns:
        NaN (np.nan): if the alpha code was not found
        country_name (string): the name of the country
    Raises:
        No exception is raised.
    """

    country_name = Country.get_country_name_from_iso3(country, use_live=False)
    if not country_name:
        return None
    return country_name


def get_alpha3_from_name(country):
    """
    Gets the alpha3 code of a country given its name.

    Parameters:
        country (string): the name of a country
    Returns:
        NaN: if the country name was not found
        alpha_code (string): the alpha3 code of the country
    Raises:
        No exception is raised.
    """

    # First, the function looks for an exact match
    alpha_code = Country.get_iso3_country_code(country)

    # Returns the alpha3 code if the country was found
    if alpha_code:
        return alpha_code

    # The exact search didn't work, execute the fuzzy search available in the api
    alpha_code = Country.get_iso3_country_code_fuzzy(country)

    # The country api returns a tuple in which the element [0] is the country code and
    # the element [1] is a True or False result for the search
    if not alpha_code[1]:
        return None

    return alpha_code[0]


def get_alpha2_from_name(country):
    """
    Gets the alpha2 code of a country given its name.

    Parameters:
        country (string): the name of a country
    Returns:
        NaN: if the country name was not found
        alpha_code (string): the alpha2 code of the country
    Raises:
        No exception is raised.
    """

    # Because there isn't a direct way to get the alpha2 code from the country's name,
    # the function looks for the alpha3 code first and then for the alpha2 code.
    alpha_code = get_alpha3_from_name(country)

    # If the alpha3 code was found, get the alpha2 code
    if not np.isnan(alpha_code):
        alpha_code = get_alpha2_from_alpha3(alpha_code)

    return alpha_code


def get_alpha2_from_alpha3(country):
    """
    Gets the alpha2 code of a country given its alpha3 code.

    Parameters:
        country (string): the alpha3 code of a country
    Returns:
        NaN: if the country was not found
        alpha_code (string): the alpha2 code of the country
    Raises:
        No exception is raised.
    """

    if not len(country) == 3:
        return None

    alpha_code = Country.get_country_info_from_iso3(country)

    # The api returns a dictionary if the country is found
    if not alpha_code:
        return None

    # The key '#country+code+v_iso2' is used to get the alpha2 code
    alpha_code = alpha_code["#country+code+v_iso2"]
    return alpha_code
