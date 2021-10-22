""" Custom exceptions for the country cleaner module.
    The methods available in the library must raise one of the exceptions below if the code fails.
"""

from financial_entity_cleaner.exceptions.exception_handler import FinancialCleanerError


class CountryIsNotAString(FinancialCleanerError):
    """The country information is not a string."""

    message = 'Invalid country: country information is not a string'


class InvalidCountry(FinancialCleanerError):
    """The country information is too small, therefore is not valid."""

    message = 'Invalid country: country information is too small.'


class CountryNotFound(FinancialCleanerError):
    """Country was not found."""

    message = 'Invalid country: country not found.'