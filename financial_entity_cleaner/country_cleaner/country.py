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
            _lettercase_output (str): indicates the letter case (lower, by default) as the result of the cleaning
                        Other options are: 'upper' and 'title'.
    """

    # Constants used interally by the class
    __ATTRIBUTE_COUNTRY_NAME = 'country_name_clean'
    __ATTRIBUTE_ALPHA2 = 'country_alpha2_clean'
    __ATTRIBUTE_ALPHA3 = 'country_alpha3_clean'

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
        self._lettercase_output = LOWER_LETTER_CASE

        # Define the name of the output attributes for country name, alpha2 and alpha3
        self._country_name_output = self.__ATTRIBUTE_COUNTRY_NAME
        self._country_alpha2_output = self.__ATTRIBUTE_ALPHA2
        self._country_alpha3_output = self.__ATTRIBUTE_ALPHA3

    # Setters and Getters for the properties, so to allow user to setup the library according to his/her needs.
    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, new_mode):
        self._mode = new_mode

    @property
    def lettercase_output(self):
        return self._lettercase_output

    @lettercase_output.setter
    def lettercase_output(self, new_value):
        self._lettercase_output = new_value

    @property
    def country_name_output(self):
        return self._country_name_output

    @country_name_output.setter
    def country_name_output(self, new_value):
        self._country_name_output = new_value

    @property
    def country_alpha2_output(self):
        return self._country_alpha2_output

    @country_alpha2_output.setter
    def country_alpha2_output(self, new_value):
        self._country_alpha2_output = new_value

    @property
    def country_alpha3_output(self):
        return self._country_alpha3_output

    @country_alpha3_output.setter
    def country_alpha3_output(self, new_value):
        self._country_alpha3_output = new_value

    def __is_country_param_valid(self, country):
        """
        This internal method perform basic checking on the country information passed as parameter.

        Parameters:
            country (str): a string with country info (name or alpha codes)

        Returns:
            (bool)  True if the country passed the validation or False, otherwise
        Raises:
            CountryIsNotAString: if the country parameter is not a string and ModeOfUse=EXCEPTION_MODE
            InvalidCountry: if the country parameter is invalid due to its size and ModeOfUse=EXCEPTION_MODE \ZXC VB -
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
            CountryNotFound: when [ModeOfUse.EXCEPTION_MODE] and the country was not found
        """

        # Default Null country info
        country_name = np.nan
        alpha2_name = np.nan
        alpha3_name = np.nan
        null_dict_country = {self._country_name_output: country_name,
                             self._country_alpha2_output: alpha2_name,
                             self._country_alpha3_output: alpha3_name}

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
            dict_country = {self._country_name_output: country_name,
                            self._country_alpha2_output: alpha2_name,
                            self._country_alpha3_output: alpha3_name}
            # Apply the requested letter case
            # By default the function returns the result in lower case
            for key, value in dict_country.items():
                if self._lettercase_output == UPPER_LETTER_CASE:
                    dict_country[key] = value.upper()
                elif self._lettercase_output == LOWER_LETTER_CASE:
                    dict_country[key] = value.lower()
                elif self._lettercase_output == TITLE_LETTER_CASE:
                    dict_country[key] = value.title()
            return dict_country
        else:
            if self._mode == ModeOfUse.EXCEPTION_MODE:
                raise custom_exception.CountryNotFound
            else:
                return null_dict_country

    def __get_country_info_for_df(self, country):
        """
        This is a private method that supports the apply_clean_to_df() method as a mean to unpack the dictionary
        returned by the search method get_country_info().

        Parameters:
            country (str): the value of the country attribute to be normalized
        Returns:
            country_name (str): the name of the country according to iso
            country_alpha2 (str): the alpha2 of the country according to iso
            country_alpha3 (str): the alpha3 of the country according to iso
        Raises:
            No exception is raised.
        """
        dict_country_info = self.get_country_info(country)
        country_name = dict_country_info[self._country_name_output]
        country_alpha2 = dict_country_info[self._country_alpha2_output]
        country_alpha3 = dict_country_info[self._country_alpha3_output]
        return country_name, country_alpha2, country_alpha3

    def apply_cleaner_to_df(self, df, in_country_attribute):
        """
        This method searches the complete country information (name, alpha2 and alpha3) for all entries of a
        dataframe that contains a country attribute, as a mean to normalize the data set.

        Parameters:
            df (dataframe): the input dataframe that contains the country attribute to be normalized
            in_country_attribute (str): the attribute in the dataframe that indicates the country to be searched for
        Returns:
            df (dataframe): the normalized version of the input dataframe
        Raises:
            CountryNotFoundInDataFrame: when [in_country_attribute] is not a dataframe's attribute
        """

        # Check if the country attribute exists in the dataframe
        if in_country_attribute not in df.columns:
            raise custom_exception.CountryNotFoundInDataFrame

        # Make a copy so not to change the original dataframe
        new_df = df.copy()

        # Creates the new output attribute that will have the normalized version of the country info
        new_df[self._country_name_output] = np.nan
        new_df[self._country_alpha2_output] = np.nan
        new_df[self._country_alpha3_output] = np.nan

        # Get the country info (name, alpha2 and alpha3) for all entries in the dataframe
        new_df.loc[:, [self._country_name_output, self._country_alpha2_output, self._country_alpha3_output]] = \
            [self.__get_country_info_for_df(country) for country in new_df[in_country_attribute]]

        return new_df