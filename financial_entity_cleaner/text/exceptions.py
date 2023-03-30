""" Custom exceptions for the text's name cleaner module.
    The methods available in the library must raise one of the exceptions below if the code fails.
"""

from financial_entity_cleaner.utils.error_handler import FinancialCleanerError


class CleaningRuleNotFoundInTheDictionary(FinancialCleanerError):
    """The cleaning rule informed was not found in the dictionary of cleaning rules."""

    message = "Some of the cleaning rules was not found in the dictionary."