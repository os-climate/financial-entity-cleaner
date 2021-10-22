""" This module contains implementation of CountryCleaner class """

# Import python libraries


# Import third-party libraries
import numpy as np

# Import internal libraries
from financial_entity_cleaner.utils.utils import remove_unicode, remove_extra_spaces
from financial_entity_cleaner.utils.utils import LOWER_LETTER_CASE, TITLE_LETTER_CASE, UPPER_LETTER_CASE

from financial_entity_cleaner.exceptions.exception_handler import ModeOfUse
from financial_entity_cleaner.country_cleaner import exceptions_country_cleaner as custom_exception

from financial_entity_cleaner.country_cleaner import search_country


class CountryCleaner:
    """
        Class to normalize/clean up country information.

        Attributes:
            _mode (int): defines if the cleaning task should be performed in silent or exception mode.
                         - EXCEPTION_MODE: the library throws exceptions in case of error during cleaning.
                         - SILENT_MODE: the library returns NaN as the result of the cleaning.
            _output_lettercase (str): indicates the letter case (lower, by default) as the result of the cleaning
                        Other options are: 'upper' and 'title'.
    """

    # Constants used interally by the class
    __ATTRIBUTE_COUNTRY_NAME = 'country_name'
    __ATTRIBUTE_ALPHA2 = 'country_alpha2'
    __ATTRIBUTE_ALPHA3 = 'country_alpha3'

    def __init__(self):
        """
            Constructor method.

            Parameters:
                No parameters are needed.
            Returns:
                CountryCleaner (object)
            Raises:
                No exception is raised.
        """

        # The mode property defines if exceptions must be thrown in case of errors
        # EXCEPTION_MODE is useful when debugging or building new applications
        # SILENT_MODE is prefered in production environments
        self._mode = ModeOfUse.SILENT_MODE

        # Define the letter case of the cleaning output
        self._output_lettercase = LOWER_LETTER_CASE

    # Setters and Getters for the properties, so to allow user to setup the library according to his/her needs.
    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, new_mode):
        self._mode = new_mode

    @property
    def output_lettercase(self):
        return self._output_lettercase

    @output_lettercase.setter
    def output_lettercase(self, new_value):
        self._output_lettercase = new_value

    def __is_country_param_valid(self, country):
        """
        This internal method perform basic checking on the country information passed as parameter.

        Parameters:
            country (str): a string with country info (name or alpha codes)

        Returns:
            (bool)  True if the country passed the validation or False, otherwise
        Raises:
            CountryIsNotAString: if the country parameter is not a string and ModeOfUse=EXCEPTION_MODE
            InvalidCountry: if the country parameter is invalid due to its size and ModeOfUse=EXCEPTION_MODE
        """
        if not isinstance(country, str):
            if self._mode == ModeOfUse.EXCEPTION_MODE:
                raise custom_exception.CountryIsNotAString
            else:
                return False

        # Check the size of the parameter
        if len(str(country).strip()) < 2:
            if self._mode == ModeOfUse.EXCEPTION_MODE:
                raise custom_exception.InvalidCountry
            else:
                return False

        # Passed all checks
        return True

    def get_country_info(self, country):
        """
        This method search for country information and if it is recognized, returns the complete info about the country:
        name, alpha code 2 and alpha code 3. It defers from other methods because the user can pass any country info,
        name or codes (2 and 3). The method will identify automatically the type of search to be applied.

        Parameters:
            country (str): a string with country info (name or alpha codes)
        Returns:
            dict_country (dict): return a dictionary of country info or None
                - dictionary: containing the name, alpha2 and alpha3 code if the country informed is valid
                - empty dict: if the country informed couldn't be found or the user parameter is null
        Raises:
            No exception is raised.
        """

        # Default Null country info
        country_name = np.nan
        alpha2_name = np.nan
        alpha3_name = np.nan
        null_dict_country = {self.__ATTRIBUTE_COUNTRY_NAME: country_name,
                             self.__ATTRIBUTE_ALPHA2: alpha2_name,
                             self.__ATTRIBUTE_ALPHA3: alpha3_name}

        # Check the country information passed as parameter
        is_valid_param = self.__is_country_param_valid(country)
        if not is_valid_param:
            return null_dict_country

        # Perform simple cleaning by removing unicode characters and extra spaces
        value = remove_unicode(country)
        value = remove_extra_spaces(value)

        # Call the correspondent search method, depending on the lenght of the country parameter
        if len(value) == 2:
            # Search by alpha2 code
            country_name = search_country.get_name_from_alpha2(value)
            if country_name:
                alpha2_name = value
                alpha3_name = search_country.get_alpha3_from_name(country_name)
        elif len(value) == 3:
            # Search by alpha3 code
            country_name = search_country.get_name_from_alpha3(value)
            if country_name:
                alpha3_name = value
                alpha2_name = search_country.get_alpha2_from_alpha3(alpha3_name)
        else:
            # Search by name
            alpha3_name = search_country.get_alpha3_from_name(value)
            if alpha3_name:
                alpha3_name = alpha3_name
                country_name = search_country.get_name_from_alpha3(alpha3_name)
                alpha2_name = search_country.get_alpha2_from_alpha3(alpha3_name)

        # Return all info if they were retrieved successfully
        if country_name and alpha2_name and alpha3_name:
            dict_country = {self.__ATTRIBUTE_COUNTRY_NAME: country_name,
                            self.__ATTRIBUTE_ALPHA2: alpha2_name,
                            self.__ATTRIBUTE_ALPHA3: alpha3_name}
            # Apply the requested letter case
            # By default the function returns the result in lower case
            for key, value in dict_country.items():
                if self._output_lettercase == UPPER_LETTER_CASE:
                    dict_country[key] = value.upper()
                elif self._output_lettercase == LOWER_LETTER_CASE:
                    dict_country[key] = value.lower()
                elif self._output_lettercase == TITLE_LETTER_CASE:
                    dict_country[key] = value.title()
            return dict_country
        else:
            if self._mode == ModeOfUse.EXCEPTION_MODE:
                raise custom_exception.CountryNotFound
            else:
                return null_dict_country