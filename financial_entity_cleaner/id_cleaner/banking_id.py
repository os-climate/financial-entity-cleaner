""" This module defines functions to validate official identifiers used in the banking industry."""

# Import third-party libraries
import numpy as np
from stdnum import isin, lei
from stdnum.gb import sedol

# Import internal libraries
from financial_entity_cleaner.utils import utils
from financial_entity_cleaner.exceptions.exception_handler import ModeOfUse
from financial_entity_cleaner.id_cleaner import (
    exceptions_id_cleaner as custom_exception,
)
from financial_entity_cleaner.utils.utils import (
    LOWER_LETTER_CASE,
    TITLE_LETTER_CASE,
    UPPER_LETTER_CASE,
)


class BankingIdCleaner:
    """
    Class to normalize/clean up banking id's, such as LEI, SEDOL and ISIN.

    Attributes:
        _mode (int): defines if the cleaning task should be performed in silent or exception mode.
                     - EXCEPTION_MODE: the library throws exceptions in case of error during cleaning.
                     - SILENT_MODE: the library returns NaN as the result of the cleaning.
        _id_type (str): defines the type of validation to be performed (isin, lei or sedol)
        _set_null_for_invalid_ids (bool): defines a return value equal to null value if the id is invalid
        _cleaned_id_output (str): the name of the output attribbute that indicates the cleaned id
        _validated_id_output (str): the name of the output attribbute that indicates the if the id is valid
    """

    # Constants used interally by the class
    __LEI_NAME = "lei"
    __ISIN_NAME = "isin"
    __SEDOL_NAME = "sedol"

    # Types of id validation available
    __VALIDATIONS_SUPPORTED = [__LEI_NAME, __ISIN_NAME, __SEDOL_NAME]

    # Suffix used to name the attributes for cleaned and validated id
    __ATTRIBUTE_CLEANED_ID = "id_cleaned"
    __ATTRIBUTE_VALIDATED_ID = "id_validated"

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
        self._id_type = self.__ISIN_NAME

        # Flag that indicates if the cleaned id should be set to null in case of being invalid
        self._set_null_for_invalid_ids = False

        # Define the name of the output attributes for cleaned and validated id
        self._cleaned_id_output = self.__ATTRIBUTE_CLEANED_ID
        self._validated_id_output = self.__ATTRIBUTE_VALIDATED_ID

        # Define the letter case of the cleaning output
        self._lettercase_output = UPPER_LETTER_CASE

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, new_mode):
        self._mode = new_mode

    @property
    def id_type(self):
        return self._id_type

    @id_type.setter
    def id_type(self, new_id_type):
        if not (new_id_type in self.__VALIDATIONS_SUPPORTED):
            raise custom_exception.TypeOfBankingIdNotSupported
        self._id_type = new_id_type

    @property
    def set_null_for_invalid_ids(self):
        return self._set_null_for_invalid_ids

    @set_null_for_invalid_ids.setter
    def set_null_for_invalid_ids(self, new_value):
        self._set_null_for_invalid_ids = new_value

    @property
    def cleaned_id_output(self):
        return self._cleaned_id_output

    @cleaned_id_output.setter
    def cleaned_id_output(self, new_value):
        self._cleaned_id_output = new_value

    @property
    def validated_id_output(self):
        return self._validated_id_output

    @validated_id_output.setter
    def validated_id_output(self, new_value):
        self._validated_id_output = new_value

    @property
    def lettercase_output(self):
        return self._lettercase_output

    @lettercase_output.setter
    def lettercase_output(self, new_value):
        self._lettercase_output = new_value

    def __validate_id(self, id_value):
        """
        Validates an official id.

        Parameters:
            id_value (str): the id to be validated
        Returns:
            (list) returns a list indicating if the id is valid and the cleaning string for that id
        Raises:
            BankingIdIsNotAString: if the id is not a string and ModeOfUse.EXCEPTION_MODE
            BankingIdIsEmptyAfterCleaning: if the id is empty after cleaning and ModeOfUse.EXCEPTION_MODE
        """
        if not isinstance(id_value, str):
            if self._mode == ModeOfUse.EXCEPTION_MODE:
                raise custom_exception.BankingIdIsNotAString
            else:
                return None

        clean_id = utils.perform_basic_cleaning(id_value)

        if len(str(clean_id).strip()) == 0:
            if self._mode == ModeOfUse.EXCEPTION_MODE:
                raise custom_exception.BankingIdIsEmptyAfterCleaning
            else:
                return None

        is_valid_id = False
        if self._id_type == self.__LEI_NAME:
            is_valid_id = lei.is_valid(clean_id)
        elif self._id_type == self.__ISIN_NAME:
            is_valid_id = isin.is_valid(clean_id)
        elif self._id_type == self.__SEDOL_NAME:
            is_valid_id = sedol.is_valid(clean_id)

        if self._lettercase_output == UPPER_LETTER_CASE:
            clean_id = clean_id.upper()
        elif self._lettercase_output == LOWER_LETTER_CASE:
            clean_id = clean_id.lower()
        elif self._lettercase_output == TITLE_LETTER_CASE:
            clean_id = clean_id.title()

        return [is_valid_id, clean_id]

    def get_clean_id(self, id_value):
        """
        Returns a clean id and if that id is valid or not. If the property [self._set_null_for_invalid_ids]
        is set to [True] the cleaned id will be set to np.nan if invalid.

        Parameters:
            id_value (str): the id to be validated
        Returns:
            dict_clean_id (dict): returns a dictionary with two attributes to indicate the cleaned id and if it is
                valid or not.
        Raises:
            No exception raised.
        """
        # Cleans up and Validates the id
        validation_return = self.__validate_id(id_value)

        # Creates an empty dict that will hold the return values for cleaned and validated id
        dict_clean_id = {
            self._cleaned_id_output: np.nan,
            self._validated_id_output: np.nan,
        }

        # Check if the validation was performed an in case of null values, return a null dict result
        if not validation_return:
            return dict_clean_id

        # If the validation was performed, get the return values
        is_valid_id = validation_return[0]
        clean_id = validation_return[1]

        # Check if the the cleaned return value should be set to null if invalid
        if self._set_null_for_invalid_ids and not is_valid_id:
            dict_clean_id[self._validated_id_output] = is_valid_id
        else:
            dict_clean_id[self._cleaned_id_output] = clean_id
            dict_clean_id[self._validated_id_output] = is_valid_id
        return dict_clean_id

    def is_valid_id(self, id_value):
        """
        Returns True if the id is valid or False otherwise. If the id is empty, returns np.nan

        Parameters:
            id_value (str): the id to be validated
        Returns:
            is_valid_id (bool): True if the id is valid or False otherwise
        Raises:
            No exception raised.
        """
        validation_return = self.__validate_id(id_value)
        is_valid_id = validation_return[0]
        if not validation_return:
            return np.nan
        return is_valid_id

    def get_types_id_validations(self):
        """
        Returns the types of validations available in the library.

        Parameters:
            No parameters required.
        Returns:
            self.__VALIDATIONS_SUPPORTED (list): the list of id types supported by the library
        Raises:
            No exception raised.
        """
        return self.__VALIDATIONS_SUPPORTED

    def __get_cleaned_validated_id_for_df(self, in_id):
        """
        This is a private method that supports the apply_clean_to_df() method as a mean to unpack the dictionary
        returned by the search method get_clean_id().

        Parameters:
            in_id (str): the attribute in the dataframe that indicates the id to be cleaned up and validated
        Returns:
            cleaned_id (str): the cleaned version of the id
            validated_id (bool): True if the id is valid and False otherwise
        Raises:
            No exception is raised.
        """
        dict_cleaned_validated_id = self.get_clean_id(in_id)
        cleaned_id = dict_cleaned_validated_id[self._cleaned_id_output]
        validated_id = dict_cleaned_validated_id[self._validated_id_output]
        return cleaned_id, validated_id

    def apply_cleaner_to_df(
        self, df, in_id_attribute, out_id_suffix_clean, out_id_suffix_valid
    ):
        """
        This method cleans up and validates ids (isin, sedol or lei) in a dataframe

        Parameters:
            df (dataframe): the input dataframe that contains the id to be clean up and validated
            in_id_attribute (str): the attributes in the dataframe that indicates the id to be cleaned and validated.
            out_id_suffix_clean (str): suffix added to the name of the id attribute in order to create a new atrribute
                in the dataframe to hold the cleaned id
            out_id_suffix_valid (str): suffix added to the name of the id attribute in order to create a new atrribute
                in the dataframe that informs if the id is valid or not
        Returns:
            df (dataframe): the cleaned and validated version of the input dataframe
        Raises:
            No exception raised.
        """
        # Check if the country attribute exists in the dataframe
        if in_id_attribute not in df.columns:
            raise custom_exception.IdNotFoundInDataFrame

        # Make a copy so not to change the original dataframe
        new_df = df.copy()

        # Defines the name of the output attributes
        new_attribute_id_cleaned = in_id_attribute + "_" + out_id_suffix_clean
        new_attribute_id_validated = in_id_attribute + "_" + out_id_suffix_valid

        # Creates the new output attribute that will have the cleaned and validated version of the input dataframe
        new_df[new_attribute_id_cleaned] = np.nan
        new_df[new_attribute_id_validated] = np.nan

        # Clean up and validate the id
        new_df.loc[:, [new_attribute_id_cleaned, new_attribute_id_validated]] = [
            self.__get_cleaned_validated_id_for_df(id_to_clean_validate)
            for id_to_clean_validate in new_df[in_id_attribute]
        ]
        return new_df
