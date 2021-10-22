""" Custom exceptions for the financial-entity-cleaner library.
The methods available in the library must raise one of the exceptions below if the code fails.
"""

from enum import Enum


class ModeOfUse(Enum):
    """
        Controls how to use the library:
        - EXCEPTION_MODE (default): exceptions are triggered whenever something bad is going on
        - SILENT_MODE: no exceptions are triggered, but instead the library returns NAN as result of bad calculations
        This mode can be very useful when running the validator or the cleaner on several entries.
    """
    EXCEPTION_MODE = 1
    SILENT_MODE = 2


class FinancialCleanerError(Exception):
    """Top-level error type of the library. This exception must not be raised.
    Instead, it is expected to use one of its subclasses. """

    def __str__(self):
        """Return the exception message."""
        return ''.join(self.args[:1]) or getattr(self, 'message', '')