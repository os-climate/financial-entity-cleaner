""" General custom exception handler for the financial-entity-cleaner library. Each package contains an exception
module with customized exception classes based on this FinancialCleanerError() class.
"""


class FinancialCleanerError(Exception):
    """Top-level error type for the entire library. This exception must not be raised.
    Instead, it is expected to use one of its subclasses. """

    def __init__(self, *args):
        self.message = ""

    def __str__(self):
        """Return the exception message."""
        if self.message:
            return 'FinancialCleanerError - ' + self.message
        else:
            return 'FinancialCleanerError has being raised - no details available.'