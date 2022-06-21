""" The **id.banking** module contains the implementation of the **BankingIdCleaner()** class which validates
official identifiers used in the banking industry. The current version of the library supports the validation of
LEI, ISIN and SEDOL identifiers.
"""

# Import third-party libraries
import numpy as np
from stdnum import isin, lei
from stdnum.gb import sedol

# Import internal libraries
from financial_entity_cleaner.utils import simple_cleaner
from financial_entity_cleaner.utils.lib import ModeOfUse, get_progress_bar, \
    TITLE_LETTER_CASE, UPPER_LETTER_CASE, LOWER_LETTER_CASE

from financial_entity_cleaner.id import exceptions as custom_exception


class BankingIdCleaner:
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
            from financial_entity_cleaner.id.banking import BankingIdCleaner
            id_cleaner = BankingIdCleaner()

            # Cleans up and validates a LEI ID:
            id_cleaner.id_type = 'lei'
            print(id_cleaner.get_clean_data('GB00B1YW4409'))

            # Validates a pandas dataframe that contains an ID column named as 'LEI':
            clean_df = id_cleaner.get_clean_df(df=not_clean_df, column_name='LEI')

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

        # The mode property defines if exceptions must be thrown in case of errors
        # EXCEPTION_MODE is useful when debugging or building new applications
        # SILENT_MODE is prefered in production environments
        self._mode = ModeOfUse.SILENT_MODE
        self._id_type = self.__ISIN_NAME

        # Flag that indicates if the cleaned id should be set to null in case of being invalid
        self._is_invalid_ids_nan = False

        # Define the name of the output attributes for cleaned and validated id
        self._output_cleaned_id = self.__ATTRIBUTE_CLEANED_ID
        self._output_validated_id = self.__ATTRIBUTE_VALIDATED_ID

        # Define the letter case of the cleaning output
        self._letter_case = UPPER_LETTER_CASE

    @property
    def mode(self):
        """
        Defines if the cleaning task should be performed in **SILENT** or **EXCEPTION** mode. To use this feature,
        import the **ModeOfUse** pre-defined class in **utils.lib** module, as shown in the example below:

        Examples:
            .. code-block:: python

                # Import the modes from utils.lib
                from financial_entity_cleaner.utils.lib import ModeOfUse

                # change the mode to show errors as exceptions
                id_cleaner.mode = ModeOfUse.EXCEPTION_MODE

                # An exception is thrown for this case
                id_cleaner.get_clean_data('xftrsss')

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
    def id_type(self):
        """
        Sets the ID type to be validated. The current version supports:

        - 'isin' : (default) validation of *Securities Identification Numbers*.
        - 'lei': validation of *Legal Entity Identifiers*.
        - 'sedol': validation of *Stock Exchange Daily Official List*


        Examples:

            .. code-block:: python

                id_cleaner.id_type = 'lei'                  # define the ID type as LEI
                id_cleaner.get_clean_data('GB00B1YW4409')   # performs the validation of the ID as LEI

        """
        return self._id_type

    @id_type.setter
    def id_type(self, new_id_type):
        if not (new_id_type in self.__VALIDATIONS_SUPPORTED):
            raise custom_exception.TypeOfBankingIdNotSupported(new_id_type)
        self._id_type = new_id_type

    @property
    def invalid_ids_as_nan(self):
        """
        If *True*, sets the return value of the cleaned ID equal to NaN if the ID is invalid, as shown below:

        .. code-block:: python

            # Result of get_info() method for an invalid ID when set_null_for_invalid_ids=True
            {'id_cleaned': nan, 'id_validated': False}

        If *False*, the return value of the cleaned ID is the cleaned version of the input ID, as shown below:

        .. code-block:: python

            # Result of get_info() method for an invalid ID when set_null_for_invalid_ids=False
            {'id_cleaned': '96XX00DPKGC9JE9F0820', 'id_validated': False}

        Examples:
            .. code-block:: python

                id_cleaner.id_type = 'lei'             # define the ID type as LEI
                id_cleaner.invalid_ids_as_nan = True   # set NaN for invalid ID
                id_cleaner.get_clean_data('XXX')       # receives NaN as result

        """
        return self._is_invalid_ids_nan

    @invalid_ids_as_nan.setter
    def invalid_ids_as_nan(self, new_value):
        self._is_invalid_ids_nan = new_value

    @property
    def output_cleaned_id(self):
        """
        The output dictionary key that identifies a cleaned ID. By default, it is defined as 'cleaned_id'.

        Examples:

            .. code-block:: python

                # Defines the output key for cleaned ID as 'NORMALIZED_ID'
                id_cleaner.output_cleaned_id = 'NORMALIZED_ID'

                 # The output key for cleaned ID is shown as 'NORMALIZED_ID'
                id_cleaner.get_clean_data('GB00B1YW4409')

        """
        return self._output_cleaned_id

    @output_cleaned_id.setter
    def output_cleaned_id(self, new_value):
        self._output_cleaned_id = new_value

    @property
    def output_validated_id(self):
        """
        The output dictionary key that identifies if the ID is valid or not. By default, it is defined as 'isvalid_id'.

        Examples:

            .. code-block:: python

                # Defines the output key for cleaned ID as 'ID_VALID'
                id_cleaner.output_validated_id = 'ID_VALID'

                 # The output key for ID validation is shown as 'ID_VALID'
                id_cleaner.get_clean_data('GB00B1YW4409')

        """
        return self._output_validated_id

    @output_validated_id.setter
    def output_validated_id(self, new_value):
        self._output_validated_id = new_value

    @property
    def letter_case(self):
        """
        Defines the letter case applied when cleaning up an ID. The options available are:

        - 'lower': (default) for an output with all characters in lower case,
        - 'upper': for an output with all characters in upper case, and
        - 'title': for an output with the first letter in upper case and the remaining ones in lowe case.

        Examples:
            .. code-block:: python

                id_cleaner.letter_case = 'upper'            # define the output in upper case
                id_cleaner.get_clean_data('GB00B1YW4409')   # cleaned ID is shown in upper case

        """
        return self._letter_case

    @letter_case.setter
    def letter_case(self, new_value):
        self._letter_case = new_value

    def __is_id_param_valid(self, id_value):
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

        if isinstance(id_value, float):
            if np.isnan(id_value):
                return False

        if not isinstance(id_value, str):
            if self._mode == ModeOfUse.EXCEPTION_MODE:
                raise custom_exception.BankingIdIsNotAString(id_value)
            else:
                return False

        clean_id = simple_cleaner.perform_basic_cleaning(id_value)

        if len(str(clean_id).strip()) == 0:
            if self._mode == ModeOfUse.EXCEPTION_MODE:
                raise custom_exception.BankingIdIsEmptyAfterCleaning(id_value)
            else:
                return False

        # Passed all checks
        return True

    def __validate_id(self, id_value):
        """
        Private method that validates an official identifier.

        Parameters:
            id_value (str): the identifier to be validated.

        Returns:
            (list): returns a list indicating if the id is valid and the cleaning string for that identifier.

        """

        clean_id = simple_cleaner.remove_unicode(id_value)
        clean_id = simple_cleaner.remove_all_spaces(clean_id)
        is_valid_id = False

        if self._id_type == self.__LEI_NAME:
            is_valid_id = lei.is_valid(clean_id)
        elif self._id_type == self.__ISIN_NAME:
            is_valid_id = isin.is_valid(clean_id)
        elif self._id_type == self.__SEDOL_NAME:
            is_valid_id = sedol.is_valid(clean_id)

        if self._letter_case == UPPER_LETTER_CASE:
            clean_id = clean_id.upper()
        elif self._letter_case == LOWER_LETTER_CASE:
            clean_id = clean_id.lower()
        elif self._letter_case == TITLE_LETTER_CASE:
            clean_id = clean_id.title()

        return [is_valid_id, clean_id]

    def reset_output_names(self):
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

    def get_clean_data(self, id_value):
        """
        Returns a clean ID and if that identifier is valid or not.

        Parameters:
            id_value (str): any string that represents an id to be validated.

        Returns:
            (dict): a dictionary with two keys that indicates the cleaned ID and if it is valid or not.
             If the property *self._is_invalid_ids_nan=True*, this method returns NaN if the id is invalid.

        Examples:

            .. code-block:: python

                # Cleans up and validates a LEI ID:
                id_cleaner.id_type = 'lei'
                print(id_cleaner.get_clean_data('GB00B1YW4409'))

                # The *print()* statement above, returns the following:
                {'cleaned_id': 'GB00B1YW4409', 'isvalid_id': 'True'}

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

    def is_valid(self, id_value):
        """
        Performs only the validation of an ID (no cleaning up).

        Parameters:
            id_value (str): any string that represents an id to be validated.

        Returns:
            (bool): *True* if the identifier is valid or *False* otherwise. If the ID is empty, returns NaN.

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

    def get_types(self):
        """
        Returns the types of identifiers that can be validated by the library.

        Returns:
            (list): returns the list of ID types supported by the library.

        """

        return self.__VALIDATIONS_SUPPORTED

    def get_clean_df(self, df, column_name):
        """
        This method performs the same process described in **get_clean_data()** method. However, the ID verification
        and cleaning are applied to a specific column of a dataframe sent by input. The output dataframe is the
        same dataframe sent by parameter, but with two new additional attributes named according to the values of
        the following properties: *output_cleaned_id*, *output_validated_id*. Therefore, you must change the values of
        these properties if you want a different column name as the result of the cleaning/validation process.

        Parameters:
            df (dataframe): the input dataframe that contains the identifier to be clean up and validated.
            column_name (str): the attribute name in the dataframe that contains the ID to be clean up and validated.

        Returns:
            (dataframe): a cleaned and validated version of the input dataframe.

        Raises:
            IdAttributeNotInDataFrame: when [column_name] is not a dataframe's column.

        Examples:
            .. code-block:: python

                # Normalizes the column named "COUNTRY" in the dataframe passed as parameter
                id_cleaner.id_type = 'isin'
                clean_df = id_cleaner.get_clean_df(my_df, "ID_ISIN")
                clean_df.head()

        """
        # Check if the country attribute exists in the dataframe
        if column_name not in df.columns:
            raise custom_exception.IdAttributeNotInDataFrame(column_name)

        # Make a copy so not to change the original dataframe
        new_df = df.copy()

        # Check if the column name is the same of the output columns
        new_col_name = ''
        if column_name == self._output_cleaned_id:
            new_col_name = column_name + "_to_remove"
            new_df.rename(columns={column_name: new_col_name}, inplace=True)
            column_name = new_col_name

        # Creates the new output attribute that will have the cleaned and validated version of the input dataframe
        new_df[self._output_cleaned_id] = np.nan
        new_df[self._output_validated_id] = np.nan

        # Clean up and validate the id
        for index, row in get_progress_bar(it_range=new_df.iterrows(),
                                           total_rows=new_df.shape[0],
                                           desc='Normalizing IDs...'):
            id_info = self.get_clean_data(row[column_name])
            if not id_info:
                id_info = {self._output_cleaned_id: np.nan, self._output_validated_id: np.nan}
            new_df.loc[index, self._output_cleaned_id] = id_info[self._output_cleaned_id]
            new_df.loc[index, self._output_validated_id] = id_info[self._output_validated_id]

        # Check if the original input column must be removed (only happens if the user asked to reused the
        # same column as ouput)
        if new_col_name != '':
            new_df.drop(new_col_name, inplace=True, axis=1)

        return new_df
