""" If **AutoCleaner()** is set to run in EXCEPTION_MODE, the library throws the custom exceptions
defined in this module.
"""

from financial_entity_cleaner.utils.error_handler import FinancialCleanerError


class SettingsNotDefined(FinancialCleanerError):
    """Settings file not defined."""

    def __init__(self, *args):
        super().__init__('AutoCleaner', args)
        self.message = "The cleaning settings file is not defined."


class NotAFolderOrFile(FinancialCleanerError):
    """Not a folder or file"""

    def __init__(self, *args):
        super().__init__('AutoCleaner', args)
        self.message = "The <{0}> is not an existent folder or file.".format(args[0])


class SettingsFileTypeNotSupported(FinancialCleanerError):
    """The file type is not supported for the cleaning settings"""

    def __init__(self, *args):
        super().__init__('AutoCleaner', args)
        self.message = "The format <{0}> is not supported. It should be .json or .yaml file.".format(args[0])


class InputFileNotFound(FinancialCleanerError):
    """The input file was not found"""

    def __init__(self, *args):
        super().__init__('AutoCleaner', args)
        self.message = "The input file was not found for the received parameter: <{0}>.".format(args[0])
