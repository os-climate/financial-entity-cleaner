""" The **id.banking** module contains the implementation of the **BankingIdCleaner()** class which validates
official identifiers used in the banking industry. The current version of the library supports the validation of
LEI, ISIN and SEDOL identifiers.
"""

from typing import Union, Tuple, List, Dict

import numpy as np
import pandas as pd
from stdnum import isin, lei
from stdnum.gb import sedol

from financial_entity_cleaner.utils.utility import get_progress_bar, get_missing_items
from financial_entity_cleaner.utils import BaseCleaner
from financial_entity_cleaner.text import SimpleCleaner

from financial_entity_cleaner.id import _exceptions as custom_exception


class BankingIdCleaner(BaseCleaner):
    """
    Class used to standardize banking id's, such as: LEI, SEDOL and ISIN.

    Given any string that represents a banking ID and informing its type, this class cleans up and validated the ID.
    The cleaning process is very simple and only removes extra spaces, strange characters and standardize the
    ID's letter case.

    The code below shows how to apply BankingIdCleaner() to standardize single string values or a specific attribute
    in a pandas dataframe structure.

    Examples:
        .. code-block:: python

            # Creates a BankingIdCleaner() object
            from financial_entity_cleaner.id import BankingIdCleaner
            id_cleaner = BankingIdCleaner()

            # Cleans up and validates a LEI ID:
            id_cleaner.id_type = 'lei'
            print(id_cleaner.clean('GB00B1YW4409'))

            # Validates a pandas dataframe that contains two ID columns of the types 'lei' and 'isin':
            clean_df = id_cleaner.clean_df(df=not_clean_df, cols=['NUM_LEI', 'NUM_ISIN'], types=['lei', 'isin'])

    """

    # Constants used interally by the class
    __LEI_NAME = "lei"
    __ISIN_NAME = "isin"
    __SEDOL_NAME = "sedol"

    # Types of id validation available
    __VALIDATIONS_SUPPORTED = [__LEI_NAME, __ISIN_NAME, __SEDOL_NAME]

    # Suffix used to name the attributes for cleaned and validated id
    __ATTRIBUTE_CLEANED_ID = "cleaned_id"
    __ATTRIBUTE_VALIDATED_ID = "isvalid_id"

    def __init__(self):

        super().__init__()

        # Default mode as silent
        self._mode = self.SILENT_MODE

        # Default type as 'isin'
        self._id_type = self.__ISIN_NAME

        # By default, invalid ID's are not set to NaN
        self._is_invalid_ids_nan = False

        # By default, the validation of ID is returned as boolean, not as 0 or 1's
        self._validation_as_categorical = False

        # Set the default name of the output attributes for cleaned and validated id
        self._output_cleaned_id = self.__ATTRIBUTE_CLEANED_ID
        self._output_validated_id = self.__ATTRIBUTE_VALIDATED_ID

        # Default letter case as 'upper'
        self._letter_case = self.UPPER_LETTER_CASE

    @property
    def id_type(self) -> str:
        """
        Sets the ID type to be validated. The current version supports:

        - 'isin' : (default) validation of *Securities Identification Numbers*.
        - 'lei': validation of *Legal Entity Identifiers*.
        - 'sedol': validation of *Stock Exchange Daily Official List*

        When using the cleaning method for pandas dataframe, if the parameter 'types' is not provided for the
        columns to be cleaned, then it is assumed that all of them are of the same type, as defined by this property.

        Examples:

            .. code-block:: python

                # Creates a BankingIdCleaner() object
                from financial_entity_cleaner.id import BankingIdCleaner
                id_cleaner = BankingIdCleaner()

                id_cleaner.id_type = 'lei'          # define the ID type as LEI
                id_cleaner.clean('GB00B1YW4409')    # performs the validation of the ID as LEI

        """
        return self._id_type

    @id_type.setter
    def id_type(self, new_id_type: str):
        # Make sure the new type is in lower case
        new_id_type = new_id_type.lower()

        # Chek if the new type is valid/supported
        if not (new_id_type in self.__VALIDATIONS_SUPPORTED):
            raise custom_exception.TypeOfBankingIdNotSupported(new_id_type)
        self._id_type = new_id_type

    @property
    def validation_as_categorical(self) -> bool:
        """
        Sets the return of the validation process as categorical data: 0 for False and 1 for True

        Examples:

            .. code-block:: python

                # Creates a BankingIdCleaner() object
                from financial_entity_cleaner.id import BankingIdCleaner
                id_cleaner = BankingIdCleaner()

                id_cleaner.validation_as_categorical = True # sets validation return as a categorical data
                id_cleaner.clean('GB00B1YW4409')            # returns 0 for False and 1 for True

        """
        return self._validation_as_categorical

    @validation_as_categorical.setter
    def validation_as_categorical(self, new_valid_return: bool):
        self._validation_as_categorical = new_valid_return

    @property
    def invalid_ids_as_nan(self) -> bool:
        """
        If *True*, sets the return value of the cleaned ID equal to NaN if the ID is invalid, as shown below:

        .. code-block:: python

            # Result of clean() method for an invalid ID when invalid_ids_as_nan=True
            {'cleaned_id': nan, 'isvalid_id': False}

        If *False*, the return value of the cleaned ID is the cleaned version of the input ID, as shown below:

        .. code-block:: python

            # Result of clean() method for an invalid ID when invalid_ids_as_nan=False
            {'cleaned_id': '96XX00DPKGC9JE9F0820', 'isvalid_id': False}

        Examples:
            .. code-block:: python

                id_cleaner.id_type = 'lei'              # define the ID type as LEI
                id_cleaner.invalid_ids_as_nan = True    # set NaN for invalid ID
                id_cleaner.clean('XXX')                 # receives NaN as result

        """
        return self._is_invalid_ids_nan

    @invalid_ids_as_nan.setter
    def invalid_ids_as_nan(self, new_value: bool):
        self._is_invalid_ids_nan = new_value

    @property
    def output_cleaned_id(self) -> str:
        """
        The output dictionary key that identifies a cleaned ID. By default, it is defined as 'cleaned_id'.

        Examples:

            .. code-block:: python

                # Defines the output key for cleaned ID as 'NORMALIZED_ID'
                id_cleaner.output_cleaned_id = 'NORMALIZED_ID'

                 # The output key for cleaned ID is shown as 'NORMALIZED_ID'
                id_cleaner.clean('GB00B1YW4409')

        """
        return self._output_cleaned_id

    @output_cleaned_id.setter
    def output_cleaned_id(self, new_value: str):
        self._output_cleaned_id = new_value

    @property
    def output_validated_id(self) -> str:
        """
        The output dictionary key that identifies if the ID is valid or not. By default, it is defined as 'isvalid_id'.

        Examples:

            .. code-block:: python

                # Defines the output key for cleaned ID as 'ID_VALID'
                id_cleaner.output_validated_id = 'ID_VALID'

                 # The output key for ID validation is shown as 'ID_VALID'
                id_cleaner.clean('GB00B1YW4409')

        """
        return self._output_validated_id

    @output_validated_id.setter
    def output_validated_id(self, new_value: str):
        self._output_validated_id = new_value

    def reset_output_names(self) -> None:
        """
        Resets the dictionary key that identifies the cleaned ID and if it is valid, as the result of get_clean_data()
        method. When this method runs, the keys are set back to its default names: "cleaned_id" and "isvalid_id".

        Examples:
            .. code-block:: python

                # Resets the output names
                id_cleaner.reset_output_names()

                # Shows the resultant dictionary with the default key names
                id_cleaner.get_clean_data('GB00B1YW4409')

        """
        self._output_cleaned_id = self.__ATTRIBUTE_CLEANED_ID
        self._output_validated_id = self.__ATTRIBUTE_VALIDATED_ID

    def __is_id_param_valid(self, id_value: Union[str, float]) -> bool:
        """
        Private method that validates an official identifier.

        Parameters:
            id_value (str): the identifier to be validated.

        Returns:
            (bool): True if is valid or False otherwise.

        Raises:
            BankingIdIsNotAString: If the id is not a string and ModeOfUse.EXCEPTION_MODE.
            BankingIdIsEmptyAfterCleaning: If the id is empty after cleaning and ModeOfUse.EXCEPTION_MODE.
        """

        # Checking if the ID is a float number is the same as checking if the ID is NaN,
        # which can be very common when cleaning up dataframes
        if isinstance(id_value, float):
            if np.isnan(id_value):
                return False

        if not isinstance(id_value, str):
            if self._mode == self.EXCEPTION_MODE:
                raise custom_exception.BankingIdIsNotAString(id_value)
            else:
                return False

        # Apply some default cleaning rules
        clean_id = SimpleCleaner.remove_unicode(id_value)
        clean_id = SimpleCleaner.remove_extra_spaces(clean_id)

        # Check if after cleaning, the ID is an empty string
        if len(str(clean_id).strip()) == 0:
            if self._mode == self.EXCEPTION_MODE:
                raise custom_exception.BankingIdIsEmptyAfterCleaning(id_value)
            else:
                return False

        # Passed all checks
        return True

    def __validate_id(self, id_value: str) -> Tuple[Union[bool, int], str]:
        """
        Private method that validates an official identifier.

        Parameters:
            id_value (str): the identifier to be validated.

        Returns:
            (tuple): returns a tuple with the first element indicating if the id is valid and the second wiht the
            cleaning string for that identifier.

        """

        clean_id = SimpleCleaner.remove_unicode(id_value)
        clean_id = SimpleCleaner.remove_all_spaces(clean_id)
        is_valid_id = False

        # Validating the ID according to its type
        if self._id_type == self.__LEI_NAME:
            is_valid_id = lei.is_valid(clean_id)

        if self._id_type == self.__ISIN_NAME:
            is_valid_id = isin.is_valid(clean_id)

        if self._id_type == self.__SEDOL_NAME:
            is_valid_id = sedol.is_valid(clean_id)

        # Adjust the validation value to int, if required
        if self._validation_as_categorical:
            if is_valid_id:
                is_valid_id = 1
            else:
                is_valid_id = 0

        # Setting the output letter case
        if self._letter_case == self.UPPER_LETTER_CASE:
            clean_id = clean_id.upper()

        if self._letter_case == self.LOWER_LETTER_CASE:
            clean_id = clean_id.lower()

        if self._letter_case == self.TITLE_LETTER_CASE:
            clean_id = clean_id.title()

        return is_valid_id, clean_id

    def clean(self, id_value: Union[str, float]) -> Union[None, Dict[str, Union[str, Union[bool, int]]]]:
        """
        Returns a clean ID and if that identifier is valid or not.

        Parameters:
            id_value (str or float): any string that represents an id to be validated or a NaN wich is represented
            as a float number.

        Returns:
            (None or dict): a dictionary with two keys that indicates the cleaned ID and if it is valid or not.
             If the property *invalid_ids_as_nan=True* and the ID is invalid, then this method will return
             the following: {'cleaned_id': NaN, 'isvalid_id': False}
             If the id_value does not pass in the basic checking and the mode is SILENT_MODE, then this method
             will return a None object.

        Examples:

            .. code-block:: python

                # Cleans up and validates a LEI ID:
                id_cleaner.id_type = 'lei'
                print(id_cleaner.clean('GB00B1YW4409'))

                # The *print()* statement above, returns the following:
                {'cleaned_id': 'GB00B1YW4409', 'isvalid_id': True}

        """

        if not self.__is_id_param_valid(id_value):
            return None

        # Cleans up and Validates the id
        validation_return = self.__validate_id(id_value)

        # If the validation was performed, get the return values
        is_valid_id = validation_return[0]
        clean_id = validation_return[1]

        # Check if the the cleaned return value should be set to null if invalid
        dict_clean_id = {}
        if self._is_invalid_ids_nan and not is_valid_id:
            dict_clean_id[self._output_cleaned_id] = np.nan
            dict_clean_id[self._output_validated_id] = is_valid_id
        else:
            dict_clean_id[self._output_cleaned_id] = clean_id
            dict_clean_id[self._output_validated_id] = is_valid_id
        return dict_clean_id

    def is_valid(self, id_value: Union[str, float]) -> Union[None, Union[bool, int]]:
        """
        Performs only the validation of an ID (no cleaning up).

        Parameters:
            id_value (str or float):  any string that represents an id to be validated or a NaN wich is represented
            as a float number.

        Returns:
            (bool): *True* if the identifier is valid or *False* otherwise. If the ID is empty or NaN, returns None.

        Examples:

            .. code-block:: python

                # Only performs the validation of a LEI ID:
                id_cleaner.id_type = 'lei'

                # Returns 'True' because the ID is a valid LEI
                print(id_cleaner.is_valid('GB00B1YW4409'))

        """

        if not self.__is_id_param_valid(id_value):
            return None

        validation_return = self.__validate_id(id_value)
        return validation_return[0]

    def get_types(self) -> List[str]:
        """
        Returns the types of identifiers that can be validated by the library.

        Returns:
            (list): returns the list of ID types supported by the library.

        """

        return self.__VALIDATIONS_SUPPORTED

    def clean_df(self, df: pd.DataFrame,
                 cols: List[str],
                 remove_cols: bool = False,
                 output_names_as: str = 'suffix',
                 types: List[str] = None) -> pd.DataFrame:
        """
        This method performs the same process described in **clean()** method. However, the ID verification
        and cleaning are applied to columns of a dataframe. The output dataframe is a copy of the dataframe sent
        by parameter, but with additional cleaning attributes. The cleaning attributes are named according to the
        values of the properties *output_cleaned_id*, *output_validated_id* which are used as prefix or suffix of the
        new column name. Therefore, you must change the values of these properties if you want a different
        column name as the result of the cleaning/validation process.

        Parameters:
            df (pd.Dataframe): the input dataframe that contains the identifier to be clean up and validated.
            cols (List[str]): the column names in the dataframe that contains the IDs to be clean up/validated.
            remove_cols (bool): indicates if the original columns should be removed after cleaning (False as default).
            output_names_as (str): indicates how the output names *output_cleaned_id*, *output_validated_id* are
                used to name the new cleaning attributes. The accepted values are: 'prefix' or 'suffix'. The default
                is 'suffix' which means that the new columns will be added with the same name as in the original
                dataframe, but with addional suffix defined by the properties *output_cleaned_id* and
                *output_validated_id*.
            types (List[str]): the ID types of the columns to be cleaned.


        Returns:
            (pd.Dataframe): a cleaned version of the input dataframe.

        Raises:
            IdAttributeNotInDataFrame: when one column is not a dataframe's column.
            TotalIDTypesDifferFromTotalColumns: when the number of id types and columns differ.
            TypeOfBankingIdNotSupported: when the id type(s) is/are not supported.

        Examples:
            .. code-block:: python

                # Normalizes the columns "ID_ISIN1" and "ID_ISIN2" in the dataframe passed as parameter
                # For this case, it is assumed that the ID type is the one defined by the property 'type'
                id_cleaner.type = 'isin'. Also, the original columns are removed after cleaning (remove_cols=True).
                clean_df = id_cleaner.clean_df(my_df, ["ID_ISIN1", "ID_ISIN2"], True)
                clean_df.head()

        """

        # Check the argument for output name
        if output_names_as not in ['suffix', 'prefix']:
            raise custom_exception.OutputArgumentNotSupported(output_names_as)

        # Check if all colums exist in the dataframe
        missing_columns = get_missing_items(list(df.columns), cols)
        if missing_columns:
            raise custom_exception.IdAttributeNotInDataFrame(', '.join(missing_columns))

        # If types argument is not informed, use the type of the class property
        if types is None:
            types = [self._id_type] * len(cols)
        else:
            # If types argument is provided, check its size
            if len(types) != len(cols):
                raise custom_exception.TotalIDTypesDifferFromTotalColumns(len(types), len(cols))

            # Check if all types are supported
            not_supported_types = get_missing_items(self.__VALIDATIONS_SUPPORTED, types)
            if not_supported_types:
                raise custom_exception.TypeOfBankingIdNotSupported(', '.join(not_supported_types))

        # Make a copy so not to change the original dataframe
        new_df = df.copy()

        # Temporary variables
        new_col_id = ''
        new_col_valid = ''
        new_validation_cols = []

        # Get the progress bar based on the dataframe rows
        pg_bar = get_progress_bar(it_range=new_df.iterrows(), total_rows=new_df.shape[0], desc='Normalizing IDs...')

        # Clean up and validate the id
        for index, row in pg_bar:
            for column_name, type_id in zip(cols, types):
                pg_bar.set_description("Column [{}] Type [{}] ".format(column_name, type_id))
                # Clean up the column according to its type ID
                self._id_type = type_id
                id_info = self.clean(row[column_name])
                # Set NaN values if the cleaning method returns None (e.g. for null ID's)
                if id_info is None:
                    id_info = {self._output_cleaned_id: np.nan, self._output_validated_id: np.nan}
                # Set the name for the new columns that will hold the cleaning results
                if output_names_as == 'suffix':
                    new_col_id = column_name + '_' + self.output_cleaned_id
                    new_col_valid = column_name + '_' + self.output_validated_id
                if output_names_as == 'prefix':
                    new_col_id = self.output_cleaned_id + '_' + column_name
                    new_col_valid = self.output_validated_id + '_' + column_name
                # Add the new cleaning attributes to the dataframe
                new_df.loc[index, new_col_id] = id_info[self._output_cleaned_id]
                new_df.loc[index, new_col_valid] = id_info[self._output_validated_id]

                # Keep the validation colum names
                if new_col_valid not in new_validation_cols:
                    new_validation_cols.append(new_col_valid)
        # Close the progress bar
        pg_bar.close()

        # Remove the original input column if required
        if remove_cols:
            new_df.drop(cols, inplace=True, axis=1)

        # Adjust the column type for the validation values
        if not self._validation_as_categorical:
            new_df[new_validation_cols] = new_df[new_validation_cols].astype(bool)

        return new_df
