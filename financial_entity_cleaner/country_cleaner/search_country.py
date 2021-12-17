from hdx.location.country import Country


def get_name_from_alpha2(country, lookup_dict_from_web=False):
    """
    Gets the name of a country given its alpha2 code.

    Parameters:
        country (str): the alpha2 code
        lookup_dict_from_web (bool): indicates if the country lib looks up for the updated dictionary
            of countries available in the web
    Returns:
        country_name (str): the name of the country or None
    Raises:
        No exception is raised.
    """

    country_name = Country.get_country_name_from_iso2(country, use_live=lookup_dict_from_web)
    if not country_name:
        return None
    return country_name


def get_name_from_alpha3(country, lookup_dict_from_web=False):
    """
    Gets the name of a country given its alpha3 code.

    Parameters:
        country (str): the alpha3 code
        lookup_dict_from_web (bool): indicates if the country lib looks up for the updated dictionary
            of countries available in the web
    Returns:
        country_name (str): the name of the country or None
    Raises:
        No exception is raised.
    """

    country_name = Country.get_country_name_from_iso3(country, use_live=lookup_dict_from_web)
    if not country_name:
        return None
    return country_name


def get_alpha3_from_name(country, lookup_dict_from_web=False):
    """
    Gets the alpha3 code of a country given its name.

    Parameters:
        country (str): the name of a country
        lookup_dict_from_web (bool): indicates if the country lib looks up for the updated dictionary
            of countries available in the web
    Returns:
        alpha_code (str): the alpha3 code of the country or None
    Raises:
        No exception is raised.
    """

    # First, the function looks for an exact match
    alpha_code = Country.get_iso3_country_code(country, use_live=lookup_dict_from_web)

    # Returns the alpha3 code if the country was found
    if alpha_code:
        return alpha_code

    # The exact search didn't work, execute the fuzzy search available in the api
    alpha_code = Country.get_iso3_country_code_fuzzy(country, use_live=lookup_dict_from_web)

    # The country api returns a tuple in which the element [0] is the country code and
    # the element [1] is a True or False result for the search
    if not alpha_code[1]:
        return None

    return alpha_code[0]


def get_alpha2_from_name(country, lookup_dict_from_web=False):
    """
    Gets the alpha2 code of a country given its name.

    Parameters:
        country (str): the name of a country
        lookup_dict_from_web (bool): indicates if the country lib looks up for the updated dictionary
            of countries available in the web
    Returns:
        alpha_code (str): the alpha2 code of the country or None
    Raises:
        No exception is raised.
    """

    # Because there isn't a direct way to get the alpha2 code from the country's name,
    # the function looks for the alpha3 code first and then for the alpha2 code.
    alpha_code = get_alpha3_from_name(country, lookup_dict_from_web)

    # If the alpha3 code was not found, return nan
    if not alpha_code:
        return None

    # Alpha3 was found, therefore get the alpha2 code
    alpha_code = get_alpha2_from_alpha3(alpha_code, lookup_dict_from_web)
    if not alpha_code:
        return None

    return alpha_code


def get_alpha2_from_alpha3(country, lookup_dict_from_web=False):
    """
    Gets the alpha2 code of a country given its alpha3 code.

    Parameters:
        country (str): the alpha3 code of a country
        lookup_dict_from_web (bool): indicates if the country lib looks up for the updated dictionary
            of countries available in the web
    Returns:
        alpha_code (str): the alpha2 code of the country or None
    Raises:
        No exception is raised.
    """

    alpha_code = Country.get_country_info_from_iso3(country, use_live=lookup_dict_from_web)

    # The api returns a dictionary if the country is found
    if not alpha_code:
        return None

    # The key '#country+code+v_iso2' is used to get the alpha2 code
    alpha_code = alpha_code["#country+code+v_iso2"]
    return alpha_code
