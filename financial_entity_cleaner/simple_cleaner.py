""" This module defines basic clean up functions """

# Import python libraries
import re
import logging

# Initialize logger object
logger = logging.getLogger(__name__)


def clean_unicode(str_value):
    """
    Removes unicode character that is unreadable when converted to ASCII format.

    Parameters:
        str_value (string): any string containing unicode characters
    Returns:
        clean_value (string): a string without unicode characters
    Raises:
        AttributeError: when [str_value] is not of a string type
    """
    if not isinstance(str_value, str):
        logger.error("Unicode cleaning cannot be applied to non string values.")
        raise AttributeError

    clean_value = str_value.encode("ascii", "ignore").decode()
    return clean_value


def apply_cleaning_rules(str_value, dict_cleaning_rules):
    """
    Applies several cleaning rules based on a custom dictionary sent by parameter.
    The dictionary contains the cleaning rules written in regex.
    See cleaner_data.py for an example of a custom cleaning rule dictionary.

    Parameters:
        str_value (string): any string
        dict_cleaning_rules (dictionary): a dictionary with cleaning rules written in regex.
        Example:
            [dictionary_name] = [rule name] : [two-element list: 'replacement', 'regex rule']
            cleaning_rules = {'remove_email': ['', '[.\w]@[.\w]'],
                              'remove_www_address': ['', 'https?://[.\w]{3,}|www.[.\w]{3,}']}
    Returns:
        clean_value (string): a modified string
    Raises:
        AttributeError: when [str_value] is not of a string type
    """
    if not isinstance(str_value, str):
        logger.error("Cleaning rules cannot be applied to non string values.")
        raise AttributeError

    clean_value = str_value
    # Iterate through the dictionary and apply each regex rule
    for name_rule, cleaning_rule in dict_cleaning_rules.items():
        # First element is the replacement
        replacement = cleaning_rule[0]
        # Second element is the regex rule
        regex_rule = cleaning_rule[1]
        # Make sure to use raw string
        regex_rule = r"{}".format(regex_rule)
        # Apply the regex rule
        clean_value = re.sub(regex_rule, replacement, clean_value)

    return clean_value
