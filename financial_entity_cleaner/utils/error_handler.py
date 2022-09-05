""" General custom exception handler for the financial-entity-cleaner library. Each package contains an exception
module with customized exception classes based on this FinancialCleanerError() class.
"""


class FinancialCleanerError(Exception):
    """Top-level error type for the entire library. This exception must not be raised.
    Instead, it is expected to use one of its subclasses. """

    def __init__(self, source_name, *args):
        self.source_name = source_name
        if args[0]:
            self.message = args[0]
        else:
            self.message = ""

    def __str__(self):
        """Return the exception message."""
        if self.message:
            return 'Financial-Entity-Cleaner (Error) <{0}> - {1}'.format(self.source_name, self.message)
        else:
            return 'Financial-Entity-Cleaner error has being raised - no details available.'