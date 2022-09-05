""" If **CountryCleaner()** is set to run in EXCEPTION_MODE, the library throws custom exceptions
defined in this module.
"""

from financial_entity_cleaner.utils.error_handler import FinancialCleanerError


class CountryIsNotAString(FinancialCleanerError):
    """The input country data is not a string."""

    def __init__(self, *args):
        super().__init__('CountryCleaner', args)
        self.message = "The input data <{0}> is not a string.".format(args[0])


class CountryInputDataTooSmall(FinancialCleanerError):
    """The input data is too small to be a country data."""

    def __init__(self, *args):
        super().__init__('CountryCleaner', args)
        self.message = "The input data <{0}> is too short to be a country data.".format(args[0])


class CountryNotFound(FinancialCleanerError):
    """Country was not found."""

    def __init__(self, *args):
        super().__init__('CountryCleaner', args)
        self.message = "The country <{0}> was not found.".format(args[0])


class CountryAttributeNotInDataFrame(FinancialCleanerError):
    """Country attribute does not exist in the dataframe."""

    def __init__(self, *args):
        super().__init__('CountryCleaner', args)
        self.message = "The country attribute(s) <{0}> could not be found in the dataframe.".format(args[0])


class CountryInfoNotSupported(FinancialCleanerError):
    """Country information requested is not supported or is unknown."""

    def __init__(self, *args):
        super().__init__('CountryCleaner', args)
        self.message = "The country information requested <{}> is not supported or is unknown.".format(args[0])


class OutputArgumentNotSupported(FinancialCleanerError):
    """Output name argument not supported or is unknown."""

    def __init__(self, *args):
        super().__init__('CountryCleaner', args)
        self.message = "The argument for output name <{}> is not supported or is unknown.".format(args[0])