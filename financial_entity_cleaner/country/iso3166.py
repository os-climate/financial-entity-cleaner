""" The **country.iso3166** module contains the implementation of the **CountryCleaner()** class that provides the
normalized values of country's name, alpha2 and alpha3 codes as defined in the ISO 3166 standard."""

# Import third-party libraries
import numpy as np

# Import internal libraries
from financial_entity_cleaner.utils.simple_cleaner import remove_unicode, remove_extra_spaces
from financial_entity_cleaner.utils.lib import ModeOfUse, get_progress_bar, \
    TITLE_LETTER_CASE, UPPER_LETTER_CASE, LOWER_LETTER_CASE

from financial_entity_cleaner.country import exceptions as custom_exception
from financial_entity_cleaner.country import search_country


class CountryCleaner:
    """
    Given any string that contains country code or name (even not completed names), CountryCleaner() searches
    in its internal ISO 3166 dictionary of countries for a match. If the match is positive, it returns a dictionary
    with the following information about that country: official name, alpha2 and alpha3 codes.

    The examples below show how to apply CountryCleaner() to normalize single string values or a specific attribute in
    a pandas dataframe structure.

    Examples:
        .. code-block:: python

            # Creates a CountryCleaner() object
            from financial_entity_cleaner.country.iso3166 import CountryCleaner
            country_cleaner = CountryCleaner()

            # Normalizes a string value that contains country data:
            country_cleaner.get_info('us')

            # Normalizes a pandas dataframe that contains a country column named as 'COUNTRY_NAME':
            clean_df = country_cleaner.get_clean_df(df=not_clean_df, column_name='COUNTRY_NAME')

    """

    # Constants used interally by the class
    __ATTRIBUTE_COUNTRY_NAME = "iso_name"
    __ATTRIBUTE_ALPHA2 = "iso_alpha2"
    __ATTRIBUTE_ALPHA3 = "iso_alpha3"

    def __init__(self):
        # The mode property defines if exceptions must be thrown in case of errors
        # EXCEPTION_MODE is useful when debugging or building new applications
        # SILENT_MODE is prefered in production environments
        self._mode = ModeOfUse.SILENT_MODE

        # Define the letter case of the cleaning output
        self._letter_case = LOWER_LETTER_CASE

        # Define the name of the output attributes for country name, alpha2 and alpha3
        self._output_name = self.__ATTRIBUTE_COUNTRY_NAME
        self._output_alpha2 = self.__ATTRIBUTE_ALPHA2
        self._output_alpha3 = self.__ATTRIBUTE_ALPHA3

    # Setters and Getters for the properties, so to allow user to setup the library according to his/her needs.
    @property
    def mode(self):
        """
        Defines if the cleaning task should be performed in **SILENT** or **EXCEPTION** mode. To use this feature,
        import the **ModeOfUse** pre-defined class in **utils.lib** module, as shown in the example below:

        Examples:
            .. code-block:: python

                # Imports the modes from utils.lib
                from financial_entity_cleaner.utils.lib import ModeOfUse

                # Changes the mode to show errors as exceptions
                country_cleaner.mode = ModeOfUse.EXCEPTION_MODE

                # An exception is thrown for this case
                country_cleaner.get_info('inexistent_country')

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
        self._mode = new_mode

    @property
    def letter_case(self):
        """
        Defines the letter case applied as the result of the country's normalization. The options available are:

        - 'lower': (default) for an output with all characters in lower case,
        - 'upper': for an output with all characters in upper case, and
        - 'title': for an output with the first letter in upper case and the remaining ones in lowe case.

        Examples:
            .. code-block:: python

                country_cleaner.letter_case = 'upper'   # define the output in upper case
                country_cleaner.get_info('us')          # country's information is shown in upper case

        """
        return self._letter_case

    @letter_case.setter
    def letter_case(self, new_value):
        self._letter_case = new_value

    @property
    def output_name(self):
        """
        The dictionary key that identifies the official country name returned as part of the normalization process.

        Examples:
            .. code-block:: python

                # Defines the output key for the official name as 'NEW_COUNTRY_NAME'
                country_cleaner.output_name = 'NEW_COUNTRY_NAME'

                # The output key for the official name is shown as 'NEW_COUNTRY_NAME'
                country_cleaner.get_info('us')

        """
        return self._output_name

    @output_name.setter
    def output_name(self, new_value):
        self._output_name = new_value

    @property
    def output_alpha2(self):
        """
        The dictionary key that identifies the official alpha2 country code returned as part of the normalization
        process.

        Examples:
            .. code-block:: python

                # Defines the output key for the official alpha2 code as 'NEW_ALPHA2_CODE'
                country_cleaner.output_alpha2 = 'NEW_ALPHA2_CODE'

                # The output key for alpha2 code is shown as 'NEW_ALPHA2_CODE'
                country_cleaner.get_info('us')
        """
        return self._output_alpha2

    @output_alpha2.setter
    def output_alpha2(self, new_value):
        self._output_alpha2 = new_value

    @property
    def output_alpha3(self):
        """
        The dictionary key that identifies the official alpha3 country code returned as part of the normalization
        process.

        Examples:
            .. code-block:: python

                # Defines the output key for the official alpha3 code as 'NEW_ALPHA3_CODE'
                country_cleaner.output_alpha3 = 'NEW_ALPHA3_CODE'

                # The output key for alpha3 code is shown as 'NEW_ALPHA3_CODE'
                country_cleaner.get_info('us')

        """
        return self._output_alpha3

    @output_alpha3.setter
    def output_alpha3(self, new_value):
        self._output_alpha3 = new_value

    def __is_country_param_valid(self, country):
        """
        This internal method performs basic checking on the country information passed as parameter.

        Parameters:
            country (str): a string with country info (name or alpha codes)

        Returns:
            (bool): True if the country passed the validation or False, otherwise

        Raises:
            CountryIsNotAString: if the country parameter is not a string and ModeOfUse=EXCEPTION_MODE
            InvalidCountry: if the country parameter is invalid due to its size and ModeOfUse=EXCEPTION_MODE

        """
        if not isinstance(country, str):
            if self._mode == ModeOfUse.EXCEPTION_MODE:
                raise custom_exception.CountryIsNotAString(country)
            else:
                return False

        # Check the size of the parameter
        if len(str(country).strip()) < 2:
            if self._mode == ModeOfUse.EXCEPTION_MODE:
                raise custom_exception.CountryInputDataTooSmall(country)
            else:
                return False

        # Passed all checks
        return True

    def reset_output_names(self):
        """
        Resets the dictionary key that identifies the official name, alpha2 and alpha3 codes returned as part of
        the normalization process. When this method runs, the keys are set back to its default names: "iso_name",
        "iso_alpha2" and "iso_alpha3".

        Examples:
            .. code-block:: python

                # Resets the output names
                country_cleaner.reset_output_names()

                # Shows the resultant dictionary with the default key names
                country_cleaner.get_info('us')

        """
        self._output_name = self.__ATTRIBUTE_COUNTRY_NAME
        self._output_alpha2 = self.__ATTRIBUTE_ALPHA2
        self._output_alpha3 = self.__ATTRIBUTE_ALPHA3

    def get_info(self, country):
        """
        This method searches for country information and if the match is positive, it returns the following information
        about the country: name, alpha2 and alpha3 codes. The user can pass any country data as input, even incomplete
        names. The method identifies automatically the best research type (by name or code) and in case of searching by
        name, a fuzzy search algorithm is applied to retrieve the most relevant match.

        Parameters:
            country (str): any string with country information (name or alpha codes)

        Returns:
            (dict): a dictionary of country information or None. See below an example of a positive match: \n
            .. code-block:: python

                {'iso_name': 'portugal', 'iso_alpha2': 'pt', 'iso_alpha3': 'prt'}

            Now, see below an example on how to test for a failed search: \n
            .. code-block:: python

                country_info = country_cleaner.get_info('test')
                if country_info is None:
                   print('Country was not found')

        Raises:
            CountryNotFound: this pre-defined exception is raised only when [ModeOfUse.EXCEPTION_MODE] is set and
            the search for the given country has failed.

        Examples:
            .. code-block:: python

                # Looks for a country associated to 'pt' (Portugal)
                country_cleaner.get_info('pt')

        """

        # Default Null country info
        country_name = np.nan
        alpha2_name = np.nan
        alpha3_name = np.nan

        # Check the country information passed as parameter
        is_valid_param = self.__is_country_param_valid(country)
        if not is_valid_param:
            return None

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
            dict_country = {
                self._output_name: country_name,
                self._output_alpha2: alpha2_name,
                self._output_alpha3: alpha3_name,
            }
            # Apply the requested letter case
            # By default the function returns the result in lower case
            for key, value in dict_country.items():
                if self._letter_case == UPPER_LETTER_CASE:
                    dict_country[key] = value.upper()
                elif self._letter_case == LOWER_LETTER_CASE:
                    dict_country[key] = value.lower()
                elif self._letter_case == TITLE_LETTER_CASE:
                    dict_country[key] = value.title()
            return dict_country
        else:
            if self._mode == ModeOfUse.EXCEPTION_MODE:
                raise custom_exception.CountryNotFound(country)
            else:
                return None

    def __get_info_for_df(self, country):
        """
        This is an internal method that supports get_clean_df() method as a mean to treat the case where get_info()
        method returns None (country was not found). In this case, a dictionary of NaN objects is returned to fill
        out the row in the dataframe.

        Parameters:
            country (str): the value of the country attribute to be normalized

        Returns:
            (dict): return the dictionary of country info or full of NaN objects

        """
        dict_country_info = self.get_info(country)
        if dict_country_info is None:
            dict_country_info = {self._output_name: np.nan,
                                 self._output_alpha2: np.nan,
                                 self._output_alpha3: np.nan}
        return dict_country_info

    def get_clean_df(self, df, column_name):
        """
        This method performs the same country search as described in get_info() method. However, the country
        normalization is applied to a specific column of a dataframe sent by input. The output dataframe is the
        same dataframe sent by parameter, but with three new additional attributes for the normalized name, alpha2
        and alpha3 codes. You can use the methods output_name, output_alpha2 and output_alpha3 to give meaningfull
        names to the output fields.

        Parameters:
            df (dataframe): the input dataframe that contains the country attribute to be normalized
            column_name (str): the attribute name in the dataframe that contains some country data to be searched.
              Notice that the dataframe column can contain any mix of country data (names or codes all mixed up).

        Returns:
            (pandas dataframe): the normalized version of the input dataframe

        Raises:
            CountryNotFoundInDataFrame: when [column_name] is not a dataframe's column.
            CountryNotFound: when [ModeOfUse.EXCEPTION_MODE] and the country was not found.

        Examples:
            .. code-block:: python

                # Normalizes the column named "COUNTRY" in the dataframe passed as parameter
                clean_df = country_cleaner.get_clean_df(my_df, "COUNTRY")
        """

        # Check if the country attribute exists in the dataframe
        if column_name not in df.columns:
            raise custom_exception.CountryAttributeNotInDataFrame(column_name)

        # Make a copy so not to change the original dataframe
        new_df = df.copy()

        # Creates the new output attribute that will have the normalized version of the country info
        new_df[self._output_name] = np.nan
        new_df[self._output_alpha2] = np.nan
        new_df[self._output_alpha3] = np.nan

        # Get the country info (name, alpha2 and alpha3) for each entry in the dataframe
        for index, row in get_progress_bar(it_range=new_df.iterrows(),
                                           total_rows=new_df.shape[0],
                                           desc='Normalizing countries...'):
            country_info = self.__get_info_for_df(row[column_name])
            new_df.loc[index, self._output_name] = country_info[self._output_name]
            new_df.loc[index, self._output_alpha2] = country_info[self._output_alpha2]
            new_df.loc[index, self._output_alpha3] = country_info[self._output_alpha3]
        return new_df
