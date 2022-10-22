""" The **location.country** module contains the implementation of the **CountryCleaner()** class that provides the
normalized values of country's name, alpha2 and alpha3 codes as defined in the ISO 3166 standard."""

from typing import Union, List, Dict
import numpy as np
import pandas as pd

from financial_entity_cleaner.utils.utility import get_progress_bar, get_missing_items
from financial_entity_cleaner.utils import BaseCleaner
from financial_entity_cleaner.text import SimpleCleaner

from financial_entity_cleaner.location import _exceptions as custom_exception
from financial_entity_cleaner.location import _search_country


class CountryCleaner(BaseCleaner):
    """
    Given any string that contains country code or name (even not completed names), CountryCleaner() searches
    in its internal ISO 3166 dictionary of countries for a match. If the match is positive, it returns a dictionary
    with the following information about that country: code, name, alpha2, alpha3

    The code below shows how to apply CountryCleaner() to normalize single string values or a specific attribute in
    a pandas dataframe structure.

    Examples:
        .. code-block:: python

            # Creates a CountryCleaner() object
            from financial_entity_cleaner.location import CountryCleaner
            country_cleaner = CountryCleaner()

            # Normalizes a string value that contains country data:
            print(country_cleaner.clean('us'))

            # Normalizes a pandas dataframe that contains two columns with country information:
            clean_df = country_cleaner.clean_df(df=not_clean_df, columns=['COUNTRY_01', 'COUNTRY_02'])

    """

    # Constants used interally by the class
    ATTRIBUTE_CODE = "code"
    ATTRIBUTE_NAME = "name"
    ATTRIBUTE_ALPHA2 = "alpha2"
    ATTRIBUTE_ALPHA3 = "alpha3"
    ATTRIBUTE_SHORT_NAME = "short_name"
    ATTRIBUTE_REGION_NAME = "region_name"
    ATTRIBUTE_REGION_CODE = "region_code"
    ATTRIBUTE_SUBREGION_NAME = "subregion_name"
    ATTRIBUTE_SUBREGION_CODE = "subregion_code"
    ATTRIBUTE_GEO_LATITUDE = "geo_latitude"
    ATTRIBUTE_GEO_LONGITUDE = "geo_longitude"
    ATTRIBUTE_CURRENCY_CODE = "currency_code"

    __ALL_ATTRIBUTES = [ATTRIBUTE_CODE, ATTRIBUTE_NAME, ATTRIBUTE_SHORT_NAME, ATTRIBUTE_ALPHA2, ATTRIBUTE_ALPHA3,
                        ATTRIBUTE_REGION_CODE, ATTRIBUTE_REGION_NAME, ATTRIBUTE_SUBREGION_CODE,
                        ATTRIBUTE_SUBREGION_NAME, ATTRIBUTE_GEO_LATITUDE,
                        ATTRIBUTE_GEO_LONGITUDE, ATTRIBUTE_CURRENCY_CODE]

    def __init__(self):

        super().__init__()

        # The mode property defines if exceptions must be thrown in case of errors
        # EXCEPTION_MODE is useful when debugging or building new applications
        # SILENT_MODE is prefered in production environments
        self._mode = self.SILENT_MODE

        # Define the letter case of the cleaning output
        self._letter_case = self.LOWER_LETTER_CASE

        # Define the names of the output attributes
        self._output_name = self.ATTRIBUTE_NAME
        self._output_code = self.ATTRIBUTE_CODE
        self._output_alpha2 = self.ATTRIBUTE_ALPHA2
        self._output_alpha3 = self.ATTRIBUTE_ALPHA3
        self._output_short_name = self.ATTRIBUTE_SHORT_NAME
        self._output_region_name = self.ATTRIBUTE_REGION_NAME
        self._output_region_code = self.ATTRIBUTE_REGION_CODE
        self._output_subregion_name = self.ATTRIBUTE_SUBREGION_NAME
        self._output_subregion_code = self.ATTRIBUTE_SUBREGION_CODE
        self._output_geo_latitude = self.ATTRIBUTE_GEO_LATITUDE
        self._output_geo_longitude = self.ATTRIBUTE_GEO_LONGITUDE
        self._output_currency_code = self.ATTRIBUTE_CURRENCY_CODE

        # Set the return information as all
        self._output_info = self.__ALL_ATTRIBUTES

    # Setters and Getters for the properties, so to allow user to setup the library according to his/her needs.
    @property
    def output_info(self) -> List[str]:
        """
        The type of country information to return when cleaning the data. By default it is set to None, meaning that
        the user didn't customized the output attributes and, therefore, the cleaning methods will return all info
        available for that country, such as:

        - 'name' or CountryCleaner.__ATTRIBUTE_NAME: return the official name
        - 'code' or CountryCleaner.__ATTRIBUTE_CODE: return the official code
        - 'alpha2' or CountryCleaner.__ATTRIBUTE_ALPHA2: return the alpha2 code
        - 'alpha3' or CountryCleaner.__ATTRIBUTE_ALPHA3: return the alpha3 code


        Examples:
            .. code-block:: python

                # set the return data to country's name and alpha2 code only
                country_cleaner.output_info = [CountryCleaner.__ATTRIBUTE_NAME,CountryCleaner.__ATTRIBUTE_ALPHA2]
                country_cleaner.clean('us')

                # the code below generates the same result
                country_cleaner.output_info = ['name','alpha2']
                country_cleaner.clean('us')

        """
        return self._output_info

    @output_info.setter
    def output_info(self, new_value: List[str]):
        for item in new_value:
            if item not in self.__ALL_ATTRIBUTES:
                raise custom_exception.CountryInfoNotSupported(new_value)
        self._output_info = new_value

    @property
    def output_code(self) -> str:
        """
        The dictionary key that identifies the official country code returned as part of the normalization process.

        Examples:
            .. code-block:: python

                # Defines the output key for the official name as 'NEW_COUNTRY_NAME'
                country_cleaner.output_code = 'NEW_COUNTRY_CODE'

                # The output key for the official name is shown as 'NEW_COUNTRY_CODE'
                country_cleaner.clean('us')

        """
        return self._output_code

    @output_code.setter
    def output_code(self, new_value: str):
        self._output_code = new_value

    @property
    def output_name(self) -> str:
        """
        The dictionary key that identifies the official country name returned as part of the normalization process.

        Examples:
            .. code-block:: python

                # Defines the output key for the official name as 'NEW_COUNTRY_NAME'
                country_cleaner.output_name = 'NEW_COUNTRY_NAME'

                # The output key for the official name is shown as 'NEW_COUNTRY_NAME'
                country_cleaner.clean('us')

        """
        return self._output_name

    @output_name.setter
    def output_name(self, new_value: str):
        self._output_name = new_value

    @property
    def output_short_name(self) -> str:
        """
        The dictionary key that identifies the official country name returned as part of the normalization process.

        Examples:
            .. code-block:: python

                # Defines the output key for the short name as 'NEW_COUNTRY_SHORT_NAME'
                country_cleaner.output_short_name = 'NEW_COUNTRY_SHORT_NAME'

                # The output key for the short name is shown as 'NEW_COUNTRY_SHORT_NAME'
                country_cleaner.clean('us')

        """
        return self._output_short_name

    @output_short_name.setter
    def output_short_name(self, new_value: str):
        self._output_short_name = new_value

    @property
    def output_alpha2(self) -> str:
        """
        The dictionary key that identifies the official alpha2 country code returned as part of the normalization
        process.

        Examples:
            .. code-block:: python

                # Defines the output key for the official alpha2 code as 'NEW_ALPHA2_CODE'
                country_cleaner.output_alpha2 = 'NEW_ALPHA2_CODE'

                # The output key for alpha2 code is shown as 'NEW_ALPHA2_CODE'
                country_cleaner.clean('us')
        """
        return self._output_alpha2

    @output_alpha2.setter
    def output_alpha2(self, new_value: str):
        self._output_alpha2 = new_value

    @property
    def output_alpha3(self) -> str:
        """
        The dictionary key that identifies the official alpha3 country code returned as part of the normalization
        process.

        Examples:
            .. code-block:: python

                # Defines the output key for the official alpha3 code as 'NEW_ALPHA3_CODE'
                country_cleaner.output_alpha3 = 'NEW_ALPHA3_CODE'

                # The output key for alpha3 code is shown as 'NEW_ALPHA3_CODE'
                country_cleaner.clean('us')

        """
        return self._output_alpha3

    @output_alpha3.setter
    def output_alpha3(self, new_value: str):
        self._output_alpha3 = new_value

    @property
    def output_region_name(self) -> str:
        """
        The dictionary key that identifies the country's region name returned as part of the normalization
        process.

        Examples:
            .. code-block:: python

                country_cleaner.output_region_name = 'NEW_REGION_NAME'
                country_cleaner.clean('us')

        """
        return self._output_region_name

    @output_region_name.setter
    def output_region_name(self, new_value: str):
        self._output_region_name = new_value

    @property
    def output_region_code(self) -> str:
        """
        The dictionary key that identifies the country's region code returned as part of the normalization
        process.

        Examples:
            .. code-block:: python

                country_cleaner.output_region_code = 'NEW_REGION_CODE'
                country_cleaner.clean('us')

        """
        return self._output_region_code

    @output_region_code.setter
    def output_region_code(self, new_value: str):
        self._output_region_code = new_value

    @property
    def output_subregion_name(self) -> str:
        """
        The dictionary key that identifies the country's subregion name returned as part of the normalization
        process.

        Examples:
            .. code-block:: python

                country_cleaner.output_subregion_name = 'NEW_SUBREGION_NAME'
                country_cleaner.clean('us')

        """
        return self._output_subregion_name

    @output_subregion_name.setter
    def output_subregion_name(self, new_value: str):
        self._output_subregion_name = new_value

    @property
    def output_subregion_code(self) -> str:
        """
        The dictionary key that identifies the country's subregion code returned as part of the normalization
        process.

        Examples:
            .. code-block:: python

                country_cleaner.output_subregion_code = 'NEW_SUBREGION_CODE'
                country_cleaner.clean('us')

        """
        return self._output_subregion_code

    @output_subregion_code.setter
    def output_subregion_code(self, new_value: str):
        self._output_subregion_code = new_value

    @property
    def output_geo_latitude(self) -> str:
        """
        The dictionary key that identifies the country's geo latitude returned as part of the normalization
        process.

        Examples:
            .. code-block:: python

                country_cleaner.output_geo_latitude = 'NEW_GEO_LATITUDE'
                country_cleaner.clean('us')

        """
        return self._output_geo_latitude

    @output_geo_latitude.setter
    def output_geo_latitude(self, new_value: str):
        self._output_geo_latitude = new_value

    @property
    def output_geo_longitude(self) -> str:
        """
        The dictionary key that identifies the country's geo longitude returned as part of the normalization
        process.

        Examples:
            .. code-block:: python

                country_cleaner.output_geo_longitude = 'NEW_GEO_LONGITUDE'
                country_cleaner.clean('us')

        """
        return self._output_geo_longitude

    @output_geo_longitude.setter
    def output_geo_longitude(self, new_value: str):
        self._output_geo_longitude = new_value

    @property
    def output_currency_code(self) -> str:
        """
        The dictionary key that identifies the country's currency code returned as part of the normalization
        process.

        Examples:
            .. code-block:: python

                country_cleaner.output_currency_code = 'NEW_CURRENCY_CODE'
                country_cleaner.clean('us')

        """
        return self._output_currency_code

    @output_currency_code.setter
    def output_currency_code(self, new_value: str):
        self._output_currency_code = new_value

    def __is_country_param_valid(self, country: str) -> bool:
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
            if self._mode == self.EXCEPTION_MODE:
                raise custom_exception.CountryIsNotAString(country)
            else:
                return False

        # Check the size of the parameter
        if len(str(country).strip()) < 2:
            if self._mode == self.EXCEPTION_MODE:
                raise custom_exception.CountryInputDataTooSmall(country)
            else:
                return False

        # Passed all checks
        return True

    def reset_output_info(self) -> None:
        """
        Resets the output selection in order to return all the attributes available.

        Examples:
            .. code-block:: python

                # Resets the output names
                country_cleaner.reset_output_info()

                # Shows the resultant dictionary with the default key names
                country_cleaner.clean('us')

        """
        self._output_info = self.__ALL_ATTRIBUTES

    def reset_output_names(self) -> None:
        """
        Resets the dictionary key that identifies the official name, alpha2 and alpha3 codes returned as part of
        the normalization process. When this method runs, the keys are set back to its default names: "name", "code",
        "alpha2" and "alpha3".

        Examples:
            .. code-block:: python

                # Resets the output names
                country_cleaner.reset_output_names()

                # Shows the resultant dictionary with the default key names
                country_cleaner.clean('us')

        """
        self._output_name = self.ATTRIBUTE_NAME
        self._output_code = self.ATTRIBUTE_CODE
        self._output_alpha2 = self.ATTRIBUTE_ALPHA2
        self._output_alpha3 = self.ATTRIBUTE_ALPHA3
        self._output_short_name = self.ATTRIBUTE_SHORT_NAME
        self._output_region_name = self.ATTRIBUTE_REGION_NAME
        self._output_region_code = self.ATTRIBUTE_REGION_CODE
        self._output_subregion_name = self.ATTRIBUTE_SUBREGION_NAME
        self._output_subregion_code = self.ATTRIBUTE_SUBREGION_CODE
        self._output_geo_latitude = self.ATTRIBUTE_GEO_LATITUDE
        self._output_geo_longitude = self.ATTRIBUTE_GEO_LONGITUDE
        self._output_currency_code = self.ATTRIBUTE_CURRENCY_CODE

    def clean(self, country: str) -> Union[None, Dict[str, str]]:
        """
        This method searches for country information and if the match is positive, it returns the following: code,
        name, alpha2 and alpha3 codes. The user can pass any country data as input, even incomplete names.
        The method identifies automatically the best research type (by name or code) and in case of
        searching by name, a fuzzy search algorithm is applied to retrieve the most relevant match.

        Parameters:
            country (str): any string with country information (name or alpha codes)

        Returns:
            (dict): a dictionary of country information or None. See below an example of a positive match: \n
            .. code-block:: python

                {'code': '620', 'name': 'portugal', 'alpha2': 'pt', 'alpha3': 'prt'}

            Now, see below an example on how to test for a failed search: \n
            .. code-block:: python

                country_info = country_cleaner.clean('test')
                if country_info is None:
                   print('Country was not found')

        Raises:
            CountryNotFound: this pre-defined exception is raised only in EXCEPTION_MODE and if the search
              for the given country has failed.

        Examples:
            .. code-block:: python

                # Looks for a country associated to 'pt' (Portugal)
                print(country_cleaner.clean('pt'))

        """

        # Check the country information passed as parameter
        is_valid_param = self.__is_country_param_valid(country)
        if not is_valid_param:
            return None

        # Perform simple cleaning by removing unicode characters and extra spaces
        value = SimpleCleaner.remove_unicode(country)
        value = SimpleCleaner.remove_extra_spaces(value)

        # Search for country information
        info_country = _search_country.search_country_info(value)

        # Prepare the returning info
        if pd.isna(info_country['country_name']):
            if self._mode == self.EXCEPTION_MODE:
                raise custom_exception.CountryNotFound(country)
            return None

        # Return only the required attributes
        dict_country = {}
        all_country_info = zip(self.__ALL_ATTRIBUTES,
                               [self._output_code, self._output_name,
                                self._output_short_name, self._output_alpha2,
                                self._output_alpha3, self._output_region_code,
                                self._output_region_name, self._output_subregion_code,
                                self._output_subregion_name, self._output_geo_latitude,
                                self._output_geo_longitude, self._output_currency_code],
                               [info_country['code_id'], info_country['country_name'],
                                info_country['short_name'], info_country['alpha2_code'],
                                info_country['alpha3_code'], info_country['region_code'],
                                info_country['region_name'], info_country['subregion_code'],
                                info_country['subregion_name'], info_country['geo_latitude'],
                                info_country['geo_longitude'], info_country['currency_code']])
        for return_info, output_name, search_value in all_country_info:
            if return_info in self._output_info:
                dict_country[output_name] = search_value
        # Apply the requested letter case
        # By default the function returns the result in lower case
        for key, value in dict_country.items():
            if self._letter_case == self.UPPER_LETTER_CASE:
                dict_country[key] = value.upper()
            elif self._letter_case == self.LOWER_LETTER_CASE:
                dict_country[key] = value.lower()
            elif self._letter_case == self.TITLE_LETTER_CASE:
                dict_country[key] = value.title()
        return dict_country

    def __get_clean_df(self, country: str):
        """
        This is an internal method that supports get_clean_df() method as a mean to treat the case in which
        get_clean_data() method returns None (country was not found). In this case, a dictionary of NaN objects is
        returned to fill out a row in the dataframe.

        Parameters:
            country (str): the value of the country attribute to be normalized

        Returns:
            (dict): return the dictionary of country info or full of NaN objects

        """
        dict_country_info = self.clean(country)

        # If the search failed, prepare an empty dictionary to feed the dataframe row
        if dict_country_info is None:
            dict_country_info = {}
            all_country_info = zip(self.__ALL_ATTRIBUTES,
                                   [self._output_code, self._output_name,
                                    self._output_short_name, self._output_alpha2,
                                    self._output_alpha3, self._output_region_code,
                                    self._output_region_name, self._output_subregion_code,
                                    self._output_subregion_name, self._output_geo_latitude,
                                    self._output_geo_longitude, self._output_currency_code])
            for return_info, output_name in all_country_info:
                if return_info in self._output_info:
                    dict_country_info[output_name] = np.nan
        return dict_country_info

    def clean_df(self, df: pd.DataFrame,
                 cols: List[str],
                 remove_cols: bool = False,
                 output_names_as: str = 'suffix') -> pd.DataFrame:
        """
        This method performs the same country search described in the *clean()* method. However, the country
        normalization is applied to columns of a dataframe. The output dataframe is a copy of the dataframe sent
        by parameter, but with additional cleaning attributes. The cleaning attributes are named according to the
        values of the properties *output_name*, *output_code*, *output_alpha2* and *output_alpha3* which are used
        as prefix or suffix of the new column name. Therefore, you must change the values of these properties if you
        want a different column name as the result of the cleaning.

        Parameters:
            df (pd.Dataframe): the input dataframe.
            cols (List[str]): the column names in the dataframe that contains the country to be searched for.
            remove_cols (bool): indicates if the original columns should be removed after cleaning (False as default).
            output_names_as (str): indicates how the output names are used to name the new cleaning attributes.
                The accepted values are: 'prefix' or 'suffix'. The default is 'suffix'.

        Returns:
            (pandas dataframe): the normalized version of the input dataframe

        Raises:
            CountryAttributeNotInDataFrame: when [column_name] is not a dataframe's column.
            CountryNotFound: when [ModeOfUse.EXCEPTION_MODE] and the country was not found.

        Examples:
            .. code-block:: python

                # Normalizes the column named "COUNTRY" in the dataframe passed as parameter
                clean_df = country_cleaner.clean_df(my_df, "COUNTRY")
                clean_df.head()
        """

        # Check the argument for output name
        if output_names_as not in ['suffix', 'prefix']:
            raise custom_exception.OutputArgumentNotSupported(output_names_as)

        # Check if all colums exist in the dataframe
        missing_columns = get_missing_items(list(df.columns), cols)
        if missing_columns:
            raise custom_exception.CountryAttributeNotInDataFrame(', '.join(missing_columns))

        # Make a copy so not to change the original dataframe
        new_df = df.copy()

        # Get the progress bar based on the dataframe rows
        pg_bar = get_progress_bar(it_range=new_df.iterrows(),
                                  total_rows=new_df.shape[0],
                                  desc='Normalizing countries...')

        # Get the country info (name, alpha2 and alpha3) for each entry in the dataframe
        for index, row in pg_bar:
            for column_name in cols:
                # Temporary variable to store the new column name
                new_col_name = ''

                pg_bar.set_description("Cleaning column [{}]".format(column_name))
                country_info = self.__get_clean_df(row[column_name])

                for key in country_info.keys():
                    # Set the name for the new columns that will hold the cleaning results
                    if output_names_as == 'suffix':
                        new_col_name = column_name + '_' + key
                    if output_names_as == 'prefix':
                        new_col_name = key + '_' + column_name
                    # Add the new cleaning attribute to the dataframe
                    new_df.loc[index, new_col_name] = country_info[key]

        # Close the progress bar
        pg_bar.close()

        # Remove the original input column if required
        if remove_cols:
            new_df.drop(cols, inplace=True, axis=1)

        return new_df
