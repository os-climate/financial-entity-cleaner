""" Custom exceptions for the text's name cleaner module.
    The methods available in the library must raise one of the exceptions below if the code fails.
"""

from financial_entity_cleaner.utils.error_handler import FinancialCleanerError


class CompanyNameIsNotAString(FinancialCleanerError):
    """The text name is not a string."""

    message = "The text name is not a string."


class LegalTermsDictionaryDoesNotExist(FinancialCleanerError):
    """The legal term dictionary does not exist in the module's path."""

    message = "The legal term dictionary does not exist in the library path."


class LegalTermsDictionaryNotFound(FinancialCleanerError):
    """The legal terms could not be found in the json file."""

    message = "The legal terms could not be found in the json file."


class CleaningRulesDictionaryDoesNotExist(FinancialCleanerError):
    """The cleaning rules dictionary does not exist in the module's path."""

    message = "The cleaning rules dictionary does not exist in the library path."


class CleaningRulesDictionaryNotFound(FinancialCleanerError):
    """The cleaning rules could not be found in the json file."""

    message = "The cleaning rules could not be found in the json file."


class DefaultCleaningRulesNotFound(FinancialCleanerError):
    """The list of default cleaning rules could not be found in the json file."""

    message = "The list of default cleaning rules could not be found in the json file."


class LanguageNotSupported(FinancialCleanerError):
    """The language informed is not currently supported."""

    message = "The language informed is not currently supported."


class CountryNotSupported(FinancialCleanerError):
    """The country informed is not currently supported."""

    message = "The country informed is not currently supported."


class CleaningRuleNotFoundInTheDictionary(FinancialCleanerError):
    """The cleaning rule informed was not found in the dictionary of cleaning rules."""

    message = "Some of the cleaning rules was not found in the dictionary."


class ListOfLegalTermsAvailableDoesNotExist(FinancialCleanerError):
    """The file that describes the legal terms available does not exist"""

    message = "The file that describes the legal terms available does not exist."


class CompanyNameNotFoundInDataFrame(FinancialCleanerError):
    """Company name attribute does not exist in the dataframe"""

    message = "Company name attribute does not exist in the dataframe"


class CountryNotFoundInDataFrame(FinancialCleanerError):
    """Country attribute does not exist in the dataframe"""

    message = "Country attribute does not exist in the dataframe"
