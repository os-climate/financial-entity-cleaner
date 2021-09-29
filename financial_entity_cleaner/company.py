""" This module defines functions to clean up company's name."""

# Import python libraries
import logging
import re

# Import internal libraries
from financial_entity_cleaner import cleaner_data
from financial_entity_cleaner import simple_cleaner

# Import third-party libraries

# Initialize logger object
logger = logging.getLogger(__name__)


def get_pattern_name_to_clean():
    """
    This function defines the type of patterns that can be used to name attributes related to company names.
    The main idea here is to identify automatically all the attributes in which cleaning the company's name
    makes sense.

    Parameters:

    Returns:
        pattern (list): all pattern names used to identify attributes in which the cleaning can be applied
    Raises:
        No exception is raised.
    """
    return ["company_name", "entity", "name", "company"]


def get_clean_name(company_name, normalize_legal_terms=True, output_lettercase="lower"):
    """
    This function cleans up a company's name.

    Parameters:
        company_name (string): the original company's name
        normalize_legal_terms (bool): a flag to indicate if the cleaning process must normalize
        company's legal terms. e.g. LTD => LIMITED
        output_lettercase (string): indicates the letter case (lower, by default) as the result of the cleaning
        Other options are: 'upper' and 'title'
    Returns:
        clean_company_name (string): the clean version of the company's name
    Raises:
        AttributeError: when [str_value] is not of a string type
    """

    if not isinstance(company_name, str):
        logger.error(
            "Cleaning for company name cannot be applied to non string values."
        )
        raise AttributeError

    # Remove all unicode characters in the company's name
    clean_company_name = simple_cleaner.clean_unicode(company_name)

    # Remove space in the beginning and in the end and convert it to lower case
    clean_company_name = clean_company_name.strip().lower()

    # Apply normalization for legal terms
    if normalize_legal_terms:
        # Iterate through the dictionary of legal terms
        for replacement, legal_terms in cleaner_data.legal_terms_dict.items():
            # Each replacement has a list of possible terms to be searched for
            replacement = replacement.lower()
            for legal_term in legal_terms:
                # Make sure to use raw string
                legal_term = legal_term.lower()
                # Make sure the legal term is a complete word and it's a raw string
                legal_term = "\\b" + legal_term + "\\b"
                regex_rule = r"{}".format(legal_term)
                # Apply the replacement
                clean_company_name = re.sub(regex_rule, replacement, clean_company_name)

    # Get the custom dictionary of regex rules to be applied in the cleaning
    cleaning_dict = {}
    for rule_name in cleaner_data.default_company_cleaning_rules:
        cleaning_dict[rule_name] = cleaner_data.cleaning_rules_dict[rule_name]

    # Apply all the cleaning rules
    clean_company_name = simple_cleaner.apply_cleaning_rules(
        clean_company_name, cleaning_dict
    )

    # Apply the letter case, if different from 'lower'
    if output_lettercase == "upper":
        clean_company_name = clean_company_name.upper()
    elif output_lettercase == "title":
        clean_company_name = clean_company_name.title()

    clean_company_name = clean_company_name.strip()
    clean_company_name = re.sub(r"\s+", " ", clean_company_name)

    return clean_company_name
