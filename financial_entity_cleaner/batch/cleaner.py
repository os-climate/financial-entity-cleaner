import sys
import os
import pandas as pd
import traceback
from datetime import datetime

from financial_entity_cleaner.utils import utility
from financial_entity_cleaner.company import CompanyNameCleaner
from financial_entity_cleaner.location import CountryCleaner
from financial_entity_cleaner.id import BankingIdCleaner
from financial_entity_cleaner.batch import _exceptions as custom_exception


class AutoCleaner:
    """
    Class that cleans up csv files by applying cleaning by name, location and id as specified by a json setup file.

    Attributes:

    """

    # Directory to store the logs by default
    __CURRENT_DIR = os.path.dirname(__file__) or "."
    __CURRENT_MODULE_DIR = os.path.abspath(__CURRENT_DIR)

    # Keys in the json file
    __SETUP_KEY_FILE_PROCESSING = "file_processing"
    __SETUP_KEY_ATTRIBUTE_PROCESSING = "attribute_processing"
    __SETUP_KEY_COMPANY_CLEANER = "company_cleaner"
    __SETUP_KEY_COUNTRY_CLEANER = "country_cleaner"
    __SETUP_KEY_IDS_CLEANER = "id_cleaner"

    def __init__(self):
        """
        Constructor method.

        Parameters:
            No parameters required
        Returns:
            AutoCleaner (object)
        Raises:
            No exception is raised.
        """
        # Internal dictionaries to store required settings for the cleaners by text's name, location and id
        self._setup_dict_company_cleaner = None
        self._setup_dict_country_cleaner = None
        self._setup_dict_ids_cleaner = None

        # Internal dictionary to store required settings to read and save csv files (input and output)
        self._setup_dict_file_processing = None

        # Internal dictionary to store required settings to process the attributes of the input dataset
        self._setup_dict_attribute_processing = None

        self._settings_file = ""
        self._input_filename = ""
        self._output_filename = ""

    @property
    def settings_file(self) -> str:
        return self._settings_file

    @settings_file.setter
    def settings_file(self, new_value: str):
        self._settings_file = new_value
        self.__read_cleaning_settings()

    @property
    def input_filename(self) -> str:
        return self._input_filename

    @input_filename.setter
    def input_filename(self, new_value: str):
        # if not os.path.isdir(new_value) or not os.path.isfile(new_value):
        #    raise custom_exception.NotAFolderOrFile(new_value)
        self._input_filename = new_value

    @property
    def output_filename(self) -> str:
        return self._output_filename

    @output_filename.setter
    def output_filename(self, new_value: str):
        self._output_filename = new_value

    def __read_cleaning_settings(self):
        """
        Internal method that reads the cleaning settings from a json file and store its content into
        associated dictionaries

        Returns:
            No return value.
        Raises:
            No exception is raised.
        """
        if self._settings_file == "":
            raise custom_exception.SettingsNotDefined

        # Filename and extension
        file_name, file_extension = os.path.splitext(self._settings_file)

        if file_extension == '.json':
            # Read the json file that contains the parameters for automatic cleaning
            dict_settings = utility.load_json_file(self._settings_file)
        else:
            raise custom_exception.SettingsFileTypeNotSupported(file_extension)

        self.__set_cleaning_properties(dict_settings)

    def __set_cleaning_properties(self, dict_settings):

        # Check if there is a json key to setup the file processing
        if self.__SETUP_KEY_FILE_PROCESSING in dict_settings.keys():
            self._setup_dict_file_processing = dict_settings[
                self.__SETUP_KEY_FILE_PROCESSING
            ]
        else:
            self._setup_dict_file_processing = None

        # Check if there is a json key to setup the dataset processing
        if self.__SETUP_KEY_ATTRIBUTE_PROCESSING in dict_settings.keys():
            self._setup_dict_attribute_processing = dict_settings[
                self.__SETUP_KEY_ATTRIBUTE_PROCESSING
            ]
        else:
            self._setup_dict_attribute_processing = None

        # Check if there is a json key to setup the cleaning by text's name
        if self.__SETUP_KEY_COMPANY_CLEANER in dict_settings.keys():
            self._setup_dict_company_cleaner = dict_settings[
                self.__SETUP_KEY_COMPANY_CLEANER
            ]
        else:
            self._setup_dict_company_cleaner = None

        # Check if there is a json key to setup the cleaning by location
        if self.__SETUP_KEY_COUNTRY_CLEANER in dict_settings.keys():
            self._setup_dict_country_cleaner = dict_settings[
                self.__SETUP_KEY_COUNTRY_CLEANER
            ]
        else:
            self._setup_dict_country_cleaner = None

        # Check if there is a json key to setup the cleaning by id
        if self.__SETUP_KEY_IDS_CLEANER in dict_settings.keys():
            self._setup_dict_ids_cleaner = dict_settings[self.__SETUP_KEY_IDS_CLEANER]
        else:
            self._setup_dict_ids_cleaner = None

    def __execute_cleaning_by_country(self, df):
        """
        Applies the automatic cleaning for location information

        Parameters:
            df (pandas dataframe): dataframe to be cleaned that contains location attributes to be cleaned
        Returns:
            (pandas dataframe) a new dataframe with cleaned location information
        Raises:
            No exception is raised.
        """
        # Print info
        print("Executing automatic cleaning by location", file=sys.stdout)

        country_cleaner_obj = CountryCleaner()
        country_cleaner_obj.letter_case = self._setup_dict_country_cleaner["output_letter_case"]
        country_cleaner_obj.output_info = [CountryCleaner.ATTRIBUTE_SHORT_NAME,
                                           CountryCleaner.ATTRIBUTE_ALPHA2]
        country_cleaner_obj.output_short_name = self._setup_dict_country_cleaner["name_suffix_clean"]
        country_cleaner_obj.output_alpha2 = self._setup_dict_country_cleaner["alpha2_suffix_clean"]

        if "cleaning_rules" in self._setup_dict_country_cleaner:
            country_cleaner_obj.cleaning_rules = self._setup_dict_country_cleaner["cleaning_rules"]

        # Perform the cleaning
        df = country_cleaner_obj.clean_df(df=df, cols=self._setup_dict_country_cleaner["input_countries"])
        return df

    def __execute_cleaning_by_id(self, df):
        """
        Applies the automatic cleaning for banking ids

        Parameters:
            df (pandas dataframe): dataframe to be cleaned that contains banking ids to be cleaned
        Returns:
            (pandas dataframe) a new dataframe with cleaned ids
        Raises:
            No exception is raised.
        """

        # Print info
        print("Executing automatic cleaning by id", file=sys.stdout)

        id_cleaner_obj = BankingIdCleaner()
        id_cleaner_obj.letter_case = self._setup_dict_ids_cleaner["output_letter_case"]
        id_cleaner_obj.output_cleaned_id = self._setup_dict_ids_cleaner["id_suffix_clean"]
        id_cleaner_obj.output_validated_id = self._setup_dict_ids_cleaner["id_suffix_valid"]
        id_cleaner_obj.invalid_ids_as_nan = eval(self._setup_dict_ids_cleaner["invalid_ids_as_null"])
        id_cleaner_obj.validation_as_categorical = eval(self._setup_dict_ids_cleaner["validation_as_categorical"])
        ids_attributes = self._setup_dict_ids_cleaner["input_ids"]

        # Perform convertion Siret to Siren if required
        if "convert_siret_to_siren" in self._setup_dict_ids_cleaner:
            replace_siren = eval(self._setup_dict_ids_cleaner["replace_siren_if_exists"])
            for siret_col, siren_col in self._setup_dict_ids_cleaner["convert_siret_to_siren"].items():
                df = id_cleaner_obj.siret_to_siren_df(df=df,
                                                      siret_col_name=siret_col,
                                                      siren_col_name=siren_col,
                                                      replace_if_exists=replace_siren)

        # Perform the cleaning
        df = id_cleaner_obj.clean_df(df=df,
                                     cols=list(ids_attributes.keys()),
                                     types=list(ids_attributes.values()))
        return df

    def __execute_cleaning_by_name(self, df):
        """
        Applies the automatic cleaning for text's name

        Parameters:
            df (pandas dataframe): dataframe to be cleaned that contains a text's name
        Returns:
            (pandas dataframe) a new dataframe with cleaned comapny's name
        Raises:
            No exception is raised.
        """

        # Print info
        print("Executing automatic cleaning by text name", file=sys.stdout)

        company_cleaner_obj = CompanyNameCleaner()
        company_cleaner_obj.normalize_legal_terms = eval(self._setup_dict_company_cleaner["normalize_legal_terms"])
        company_cleaner_obj.letter_case = self._setup_dict_company_cleaner["output_letter_case"]
        company_cleaner_obj.remove_unicode = eval(self._setup_dict_company_cleaner["remove_unicode_chars"])
        merge_legal_terms = eval(self._setup_dict_company_cleaner["merge_legal_terms"])
        company_cleaner_obj.remove_accents = eval(self._setup_dict_company_cleaner["remove_accents"])
        use_cleaning_country = False
        input_names = []

        if "input_names_by_country" in self._setup_dict_company_cleaner:
            use_cleaning_country = True
            input_names = self._setup_dict_company_cleaner["input_names_by_country"]

        if "input_names" in self._setup_dict_company_cleaner:
            input_names = self._setup_dict_company_cleaner["input_names"]

        if "pre_cleaning_rules" in self._setup_dict_company_cleaner:
            company_cleaner_obj.default_cleaning_rules = self._setup_dict_company_cleaner["pre_cleaning_rules"]

        if "post_cleaning_rules" in self._setup_dict_company_cleaner:
            company_cleaner_obj.post_cleaning_rules = self._setup_dict_company_cleaner["post_cleaning_rules"]

        if use_cleaning_country:
            for output_name, input_name_country in input_names.items():
                input_name = input_name_country[0]
                input_country = (input_name_country[1]
                                 + "_"
                                 + self._setup_dict_country_cleaner["alpha2_suffix_clean"])
                df = company_cleaner_obj.clean_df(df, input_name, output_name, input_country, merge_legal_terms)
        else:
            for output_name, input_name in input_names.items():
                df = company_cleaner_obj.clean_df(df, input_name, output_name, "", merge_legal_terms)
        return df

    def __execute_auto_cleaning(self, df):
        """
        Execute the automatic cleaning for location, ids and text's name

        Parameters:
            df (pandas dataframe): dataframe to be cleaned
        Returns:
            (pandas dataframe) the cleaned dataframe
        Raises:
            No exception is raised.
        """

        # If the settings for cleaning countries were provided, then perform the cleaning by location
        if self._setup_dict_country_cleaner is not None:
            df = self.__execute_cleaning_by_country(df)

        # If the settings for cleaning ids were provided, then perform the cleaning by id
        if self._setup_dict_ids_cleaner is not None:
            df = self.__execute_cleaning_by_id(df)

        # If the settings for cleaning text´s name were provided, then perform the cleaning by name
        if self._setup_dict_company_cleaner is not None:
            df = self.__execute_cleaning_by_name(df)
        return df

    def read_latest_csv_file(self, input_path):
        # Check if settings for automatic cleaning was defined
        if self._settings_file == "":
            raise custom_exception.SettingsNotDefined

        input_filename = utility.get_newest_filename(input_path,
                                                     '*' + self._setup_dict_file_processing["file_extension"],
                                                     self._setup_dict_file_processing["filename_pattern"], )
        if input_filename is None:
            raise custom_exception.InputFileNotFound(input_path)

        # Update the filename
        self.input_filename = input_filename

        # Print info
        print("Reading csv file from " + input_filename, file=sys.stdout)
        df = self.__read_csv_file(input_filename)
        return df

    def __read_csv_file(self, input_filename):
        df = pd.read_csv(
            input_filename,
            sep=self._setup_dict_file_processing["separator"],
            encoding=self._setup_dict_file_processing["encoding"],
            dtype=object,
        )
        if self._setup_dict_attribute_processing is not None:
            df = df.loc[:, list(self._setup_dict_attribute_processing.keys())].copy()
            df.columns = list(self._setup_dict_attribute_processing.values())
        return df

    def clean_file(self):
        """
        Cleans up a csv file and returns another csv files as a result of the cleaning process

        Returns:
            (csv file) the cleaned dataset in csv format
        Raises:
            No exception is raised.
        """
        try:
            df = None
            if os.path.isdir(self._input_filename):
                df = self.read_latest_csv_file(self._input_filename)

            if os.path.isfile(self._input_filename):
                df = self.__read_csv_file(self._input_filename)

            # Execute automatic cleaning
            print("Cleaning file:" + self._input_filename, file=sys.stdout)
            df_cleaned = self.__execute_auto_cleaning(df)
            if os.path.isdir(self._output_filename):
                output_dir = os.path.abspath(self._output_filename)
                current_dt = datetime.now().strftime('%d%m%Y_%H%M%S')
                in_path, filename = os.path.split(self._input_filename)
                len_extension = len(self._setup_dict_file_processing["file_extension"]) * -1
                filename = filename[:len_extension] + "_CLEAN_"
                filename = filename + current_dt + self._setup_dict_file_processing["file_extension"]
                self._output_filename = "{}{}{}".format(output_dir, os.sep, filename)

            # Print info
            print("Saving output file at " + self._output_filename, file=sys.stdout)

            # Save results to csv file
            df_cleaned.to_csv(
                self._output_filename,
                sep=self._setup_dict_file_processing["separator"],
                encoding=self._setup_dict_file_processing["encoding"],
                index=False,
                header=True,
            )
            return True
        except Exception as e:
            # Print error
            print("Error " + repr(e) + " ocurred", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return False

    def clean_df(self, df):
        """
        Cleans up a pandas dataframe and returns another dataframe as result of the cleaning process

        Parameters:
            df (pandas dataframe): dataframe to be cleaned
        Returns:
            (pandas dataframe) the cleaned dataframe
        Raises:
            No exception is raised.
        """
        try:
            # Check if settings for automatic cleaning was defined
            if self._settings_file == "":
                raise custom_exception.SettingsNotDefined

            # Execute automatic cleaning
            df_cleaned = self.__execute_auto_cleaning(df)
            return df_cleaned
        except Exception as e:
            # Print error
            print("Error " + repr(e) + " ocurred", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return None
