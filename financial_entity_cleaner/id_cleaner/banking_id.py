""" This module defines functions to validate official identifiers used in the banking industry."""

# Import third-party libraries
import numpy as np
from stdnum import isin, lei
from stdnum.gb import sedol

# Import internal libraries
from financial_entity_cleaner.utils import utils
from financial_entity_cleaner.exceptions.exception_handler import ModeOfUse
from financial_entity_cleaner.id_cleaner import exceptions_id_cleaner as custom_exception


class BankingIdCleaner:
    """
        Class to normalize/clean up banking id's, such as LEI, SEDOL and ISIN.

        Attributes:
            _mode (int): defines if the cleaning task should be performed in silent or exception mode.
                         - EXCEPTION_MODE: the library throws exceptions in case of error during cleaning.
                         - SILENT_MODE: the library returns NaN as the result of the cleaning.
    """

    # Constants used interally by the class
    __LEI_NAME = 'lei'
    __ISIN_NAME = 'isin'
    __SEDOL_NAME = 'sedol'

    __VALIDATIONS_SUPPORTED = [__LEI_NAME, __ISIN_NAME, __SEDOL_NAME]

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

        return [is_valid_id, clean_id]

    def get_clean_id(self, id_value, set_null_for_invalid=True):
        """
        Returns a clean id or np.nan if the id is null or invalid.

        Parameters:
            id_value (str): the id to be validated
            set_null_for_invalid (bool): define a return value equal to null value if the id is invalid
        Returns:
            clean_id (str): the clean id or np.nan if is empty or invalid
        Raises:
            No exception raised.
        """
        validation_return = self.__validate_id(id_value)
        is_valid_id = validation_return[0]
        clean_id = validation_return[1]
        if not validation_return:
            return [np.nan, np.nan]
        if set_null_for_invalid and not is_valid_id:
            return [is_valid_id, np.nan]
        return [is_valid_id, clean_id.upper()]

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
        return self.__VALIDATIONS_SUPPORTED