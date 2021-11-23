""" Custom exceptions for the id cleaner module.
    The methods available in the library must raise one of the exceptions below if the code fails.
"""

from financial_entity_cleaner.exceptions.exception_handler import FinancialCleanerError


class BankingIdIsNotAString(FinancialCleanerError):
    """ The Id is not a string."""

    message = 'The Id is not a string.'


class BankingIdIsEmptyAfterCleaning(FinancialCleanerError):
    """ The Id is empty after cleaning up."""

    message = 'The Id is empty after cleaning up.'


class TypeOfBankingIdNotSupported(FinancialCleanerError):
    """ The type of banking id informed is not supported."""

    message = 'The type of banking id informed is not supported.'


class IdNotFoundInDataFrame(FinancialCleanerError):
    """Id attribute does not exist in the dataframe"""

    message = 'Id attribute does not exist in the dataframe'