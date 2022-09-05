""" The **financial_entity_cleaner.utils.lib** module provides common functions that handle internal aspects of the
library, such as: library's folders and configuration files, logging and progress bars for time-consuming cleaning
processes.
"""

from financial_entity_cleaner.utils.error_handler import FinancialCleanerError


class BaseCleaner:
    """
    Base class to define other cleaner classes.
    """

    EXCEPTION_MODE = "exception"
    """
        Exceptions are triggered whenever something bad is going on.
    """

    SILENT_MODE = "silent"
    """
        No exceptions are triggered, but instead the library returns NAN as result of bad calculations
        This mode can be very useful when running the validator or the cleaner on several entries.
    """

    LOWER_LETTER_CASE = "lower"
    """
    Used to define the property **lettercase_output** that indicates the location information in lower case.

    Examples:
        >>> country_cleaner = CountryCleaner()
        >>> country_cleaner.lettercase_output = CountryCleaner.LOWER_LETTER_CASE
    """

    UPPER_LETTER_CASE = "upper"
    """
    Used to define the property **lettercase_output** that indicates the location information in upper case.

    Examples:
        >>> country_cleaner = CountryCleaner()
        >>> country_cleaner.lettercase_output = CountryCleaner.UPPER_LETTER_CASE
    """

    TITLE_LETTER_CASE = "title"
    """
    Used to define the property **lettercase_output** to indicate the location information with the first letter in 
    upper case and the remaining ones in lower case.

    Examples:
        >>> country_cleaner = CountryCleaner()
        >>> country_cleaner.lettercase_output = CountryCleaner.TITLE_LETTER_CASE
    """

    def __init__(self):

        # The mode property defines if exceptions must be thrown in case of errors
        # EXCEPTION_MODE is useful when debugging or building new applications
        # SILENT_MODE is prefered in production environments
        self._mode = self.SILENT_MODE

        # Define the letter case of the cleaning output
        self._letter_case = self.LOWER_LETTER_CASE

    @property
    def mode(self):
        """
        Defines if the cleaning task should be performed in **SILENT** or **EXCEPTION** mode. To use this feature,
        import the **ModeOfUse** pre-defined class in **utils.lib** module, as shown in the example below:

        Examples:
            .. code-block:: python

                # Import the modes from utils.lib
                from financial_entity_cleaner.utils import ModeOfUse

                # change the mode of any cleaner object to show errors as exceptions
                obj_cleaner.mode = ModeOfUse.EXCEPTION_MODE

        - **ModeOfUse.EXCEPTION_MODE**: the library *throws an exception* in case of an error during cleaning.
          The error message can be sent to the standard output or recorded in a logging file. When
          cleaning up over dataframes, the process is immediately stopped in EXCEPTION_MODE.
        - **ModeOfUse.SILENT_MODE**: the library returns *None* as the result of a failed cleaning.
          As in EXCEPTION_MODE, the error message can be sent to the standard output or recorded in a logging file.
          But, when up cleaning over dataframes, the process is immediately stopped only if the property
          *stop_if_error=True*.

        """
        return self._mode

    @mode.setter
    def mode(self, new_mode):
        if new_mode not in [self.SILENT_MODE, self.EXCEPTION_MODE]:
            raise FinancialCleanerError('Operation mode must be: exception or silent')
        self._mode = new_mode

    @property
    def letter_case(self):
        """
        Defines the letter case applied during the cleaning up on any cleaner object. The options available are:

        - 'lower': (default) for an output with all characters in lower case,
        - 'upper': for an output with all characters in upper case, and
        - 'title': for an output with the first letter in upper case and the remaining ones in lowe case.

        Examples:
            .. code-block:: python

                # Example on BankingIDCleaner
                id_cleaner.letter_case = 'upper'            # define the output in upper case
                id_cleaner.get_clean_data('GB00B1YW4409')   # cleaned ID is shown in upper case

        """
        return self._letter_case

    @letter_case.setter
    def letter_case(self, new_value):
        if new_value not in [self.LOWER_LETTER_CASE, self.UPPER_LETTER_CASE, self.TITLE_LETTER_CASE]:
            raise FinancialCleanerError('Letter case must be: lower, upper or title')
        self._letter_case = new_value