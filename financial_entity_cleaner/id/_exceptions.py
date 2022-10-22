""" If **BankingIdCleaner()** is set to run in EXCEPTION_MODE, the library throws the custom exceptions
defined in this module.
"""

from financial_entity_cleaner.utils.error_handler import FinancialCleanerError


class BankingIdIsNotAString(FinancialCleanerError):
    """The input ID is not a string."""

    def __init__(self, *args):
        super().__init__('BankingIdCleaner', args)
        self.message = "The input data <{0}> is not a string.".format(args[0])


class BankingIdIsEmptyAfterCleaning(FinancialCleanerError):
    """The ID is empty after cleaning up."""

    def __init__(self, *args):
        super().__init__('BankingIdCleaner', args)
        self.message = "The ID <{0}> is empty after cleaning up.".format(args[0])


class TypeOfBankingIdNotSupported(FinancialCleanerError):
    """The banking id types are not supported."""

    def __init__(self, *args):
        super().__init__('BankingIdCleaner', args)
        self.message = "The ID type(s) <{0}> is/are not supported.".format(args[0])


class IdAttributeNotInDataFrame(FinancialCleanerError):
    """The ID attribute does not exist in the dataframe."""

    def __init__(self, *args):
        super().__init__('BankingIdCleaner', args)
        self.message = "The ID attribute(s) <{0}> could not be found in the dataframe.".format(args[0])


class TotalIDTypesDifferFromTotalColumns(FinancialCleanerError):
    """The total ID type(s) differ from the number of columns to be cleaned."""

    def __init__(self, *args):
        super().__init__('BankingIdCleaner', args)
        self.message = "The total ID type(s)={0} differ from the number of columns={1} to be cleaned."\
            .format(args[0], args[1])


class OutputArgumentNotSupported(FinancialCleanerError):
    """Output name argument not supported or is unknown."""

    def __init__(self, *args):
        super().__init__('BankingIdCleaner', args)
        self.message = "The argument for output name <{}> is not supported or is unknown.".format(args[0])
