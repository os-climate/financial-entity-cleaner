""" If **BankingIdCleaner()** is set to run in EXCEPTION_MODE, the library throws custom exceptions
defined in this module.
"""

from financial_entity_cleaner.utils.error_handler import FinancialCleanerError


class BankingIdIsNotAString(FinancialCleanerError):
    """The input ID is not a string."""

    def __init__(self, *args):
        super().__init__(args)
        self.message = "The input data <{0}> is not a string.".format(args[0])


class BankingIdIsEmptyAfterCleaning(FinancialCleanerError):
    """The ID is empty after cleaning up."""

    def __init__(self, *args):
        super().__init__(args)
        self.message = "The ID <{0}> is empty after cleaning up.".format(args[0])


class TypeOfBankingIdNotSupported(FinancialCleanerError):
    """The banking id type is not supported."""

    def __init__(self, *args):
        super().__init__(args)
        self.message = "The ID type <{0}> is not supported.".format(args[0])


class IdAttributeNotInDataFrame(FinancialCleanerError):
    """The ID attribute does not exist in the dataframe."""

    def __init__(self, *args):
        super().__init__(args)
        self.message = "The ID attribute <{0}> does not exist in the dataframe.".format(args[0])
