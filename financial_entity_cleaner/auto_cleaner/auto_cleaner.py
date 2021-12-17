import sys
import os
import pandas as pd
import traceback

from financial_entity_cleaner.utils import utils
from financial_entity_cleaner.company_cleaner import company
from financial_entity_cleaner.country_cleaner import country
from financial_entity_cleaner.id_cleaner import banking_id


class AutoCleaner:
    """
    Class that cleans up csv files by applying cleaning by name, country and id as specified by a json setup file.

    Attributes:

    """

    # Directory to store the logs by default
    __CURRENT_DIR = os.path.dirname(__file__) or "."
    __CURRENT_MODULE_DIR = os.path.abspath(__CURRENT_DIR)
    __DEFAULT_LOGS_FOLDER = os.path.join(__CURRENT_MODULE_DIR, "logs")

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
        # Internal dictionaries to store required settings for the cleaners by company's name, country and id
        self._setup_dict_company_cleaner = None
        self._setup_dict_country_cleaner = None
        self._setup_dict_ids_cleaner = None

        # Internal dictionary to store required settings to read and save csv files (input and output)
        self._setup_dict_file_processing = None

        # Internal dictionary to store required settings to process the attributes of the input dataset
        self._setup_dict_attribute_processing = None

    def __read_cleaning_settings(self, setup_cleaning_filename):
        """
        Internal method that reads the cleaning settings from a json file and store its content into
        associated dictionaries

        Parameters:
            setup_cleaning_filename (str):  complete path and filename of a json file that contains the required
                properties on how to clean up the input file.
        Returns:
            No return value.
        Raises:
            No exception is raised.
        """
        # Print info...
        print("Reading cleaning settings from " + setup_cleaning_filename, file=sys.stdout)

        # Read the json file that contains the parameters for automatic cleaning
        dict_json = utils.load_json_file(setup_cleaning_filename)

        # Check if there is a json key to setup the file processing
        if self.__SETUP_KEY_FILE_PROCESSING in dict_json.keys():
            self._setup_dict_file_processing = dict_json[
                self.__SETUP_KEY_FILE_PROCESSING
            ]

        # Check if there is a json key to setup the dataset processing
        if self.__SETUP_KEY_ATTRIBUTE_PROCESSING in dict_json.keys():
            self._setup_dict_attribute_processing = dict_json[
                self.__SETUP_KEY_ATTRIBUTE_PROCESSING
            ]

        # Check if there is a json key to setup the cleaning by company's name
        if self.__SETUP_KEY_COMPANY_CLEANER in dict_json.keys():
            self._setup_dict_company_cleaner = dict_json[
                self.__SETUP_KEY_COMPANY_CLEANER
            ]

        # Check if there is a json key to setup the cleaning by country
        if self.__SETUP_KEY_COUNTRY_CLEANER in dict_json.keys():
            self._setup_dict_country_cleaner = dict_json[
                self.__SETUP_KEY_COUNTRY_CLEANER
            ]

        # Check if there is a json key to setup the cleaning by id
        if self.__SETUP_KEY_IDS_CLEANER in dict_json.keys():
            self._setup_dict_ids_cleaner = dict_json[self.__SETUP_KEY_IDS_CLEANER]

    def __execute_cleaning_by_country(self, df):
        """
        Applies the automatic cleaning for country information

        Parameters:
            df (pandas dataframe): dataframe to be cleaned that contains country attributes to be cleaned
        Returns:
            (pandas dataframe) a new dataframe with cleaned country information
        Raises:
            No exception is raised.
        """
        # Print info
        print("Executing automatic cleaning by country", file=sys.stdout)

        country_cleaner_obj = country.CountryCleaner()
        country_cleaner_obj.lettercase_output = self._setup_dict_country_cleaner[
            "output_letter_case"
        ]
        country_attributes = self._setup_dict_country_cleaner["input_countries"]
        for country_attribute in country_attributes:
            # For each country, setup the output name, alpha2 and alpha3 to store the cleaned values
            output_name = (
                country_attribute
                + "_"
                + self._setup_dict_country_cleaner["name_suffix_clean"]
            )
            country_cleaner_obj.country_name_output = output_name

            output_name = (
                country_attribute
                + "_"
                + self._setup_dict_country_cleaner["alpha2_suffix_clean"]
            )
            country_cleaner_obj.country_alpha2_output = output_name

            output_name = (
                country_attribute
                + "_"
                + self._setup_dict_country_cleaner["alpha3_suffix_clean"]
            )
            country_cleaner_obj.country_alpha3_output = output_name

            # Perform the cleaning
            df = country_cleaner_obj.apply_cleaner_to_df(df, country_attribute)
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

        id_cleaner_obj = banking_id.BankingIdCleaner()
        id_cleaner_obj.lettercase_output = self._setup_dict_ids_cleaner[
            "output_letter_case"
        ]
        ids_attributes = self._setup_dict_ids_cleaner["input_ids"]
        out_id_suffix_clean = self._setup_dict_ids_cleaner["id_suffix_clean"]
        out_id_suffix_valid = self._setup_dict_ids_cleaner["id_suffix_valid"]
        set_null_for_invalid_ids = eval(
            self._setup_dict_ids_cleaner["set_null_for_invalid_ids"]
        )
        id_cleaner_obj.set_null_for_invalid_ids = set_null_for_invalid_ids
        for id_attribute, id_type in ids_attributes.items():
            id_cleaner_obj.id_type = id_type
            df = id_cleaner_obj.apply_cleaner_to_df(
                df, id_attribute, out_id_suffix_clean, out_id_suffix_valid
            )
        return df

    def __execute_cleaning_by_name(self, df):
        """
        Applies the automatic cleaning for company's name

        Parameters:
            df (pandas dataframe): dataframe to be cleaned that contains a company's name
        Returns:
            (pandas dataframe) a new dataframe with cleaned comapny's name
        Raises:
            No exception is raised.
        """

        # Print info
        print("Executing automatic cleaning by company name", file=sys.stdout)

        company_cleaner_obj = company.CompanyNameCleaner()
        company_cleaner_obj.normalize_legal_terms = eval(
            self._setup_dict_company_cleaner["normalize_legal_terms"]
        )
        company_cleaner_obj.output_lettercase = self._setup_dict_company_cleaner[
            "output_letter_case"
        ]
        company_cleaner_obj.remove_unicode = eval(
            self._setup_dict_company_cleaner["remove_unicode_chars"]
        )
        if "cleaning_rules" in self._setup_dict_company_cleaner:
            cleaning_rules = self._setup_dict_company_cleaner["cleaning_rules"]
            company_cleaner_obj.default_cleaning_rules = cleaning_rules
        use_cleaning_country = eval(
            self._setup_dict_company_cleaner["use_clean_country"]
        )
        country_attribute = self._setup_dict_company_cleaner["input_country"]

        if use_cleaning_country:
            input_country = (
                country_attribute
                + "_"
                + self._setup_dict_country_cleaner["alpha2_suffix_clean"]
            )
        else:
            input_country = ""

        input_name = self._setup_dict_company_cleaner["input_company_name"]
        output_name = self._setup_dict_company_cleaner["output_company_name"]
        merge_legal_terms = eval(self._setup_dict_company_cleaner["merge_legal_terms"])

        # Creates a temporary country attribute in lower case to match the country used in the dictionaries
        if input_country != "":
            temp_input_country = input_country + "__temp"
            df[temp_input_country] = df[input_country].str.lower()
            df = company_cleaner_obj.apply_cleaner_to_df(
                df, input_name, output_name, temp_input_country, merge_legal_terms
            )
            df.drop(columns=[temp_input_country], inplace=True)
        else:
            df = company_cleaner_obj.apply_cleaner_to_df(
                df, input_name, output_name, "", merge_legal_terms
            )
        return df

    def __execute_auto_cleaning(self, df):
        """
        Execute the automatic cleaning for country, ids and company's name

        Parameters:
            df (pandas dataframe): dataframe to be cleaned
        Returns:
            (pandas dataframe) the cleaned dataframe
        Raises:
            No exception is raised.
        """

        # If the settings for selecting and renaming attributes were provided in the json file,
        # then select only the attributes of interest and rename them
        if self._setup_dict_attribute_processing:
            # Get the names of attribute to be selected from the dataset
            attributes_to_read = list(
                self._setup_dict_attribute_processing.keys()
            )  # current names
            new_attribute_names = list(
                self._setup_dict_attribute_processing.values()
            )  # new names
            # Select only the attributes of interest
            df = df[attributes_to_read]
            # Rename the columns
            df.columns = new_attribute_names

        # If the settings for cleaning countries were provided, then perform the cleaning by country
        if self._setup_dict_country_cleaner:
            df = self.__execute_cleaning_by_country(df)

        # If the settings for cleaning ids were provided, then perform the cleaning by id
        if self._setup_dict_ids_cleaner:
            df = self.__execute_cleaning_by_id(df)

        # If the settings for cleaning company´s name were provided, then perform the cleaning by name
        if self._setup_dict_company_cleaner:
            df = self.__execute_cleaning_by_name(df)

        return df

    def clean_csv_file(self, input_filename, setup_cleaning_filename, output_filename):
        """
        Cleans up a csv file and returns another csv files as a result of the cleaning process

        Parameters:
            input_filename (str): complete path and filename to be cleaned in csv format
            setup_cleaning_filename (str): complete path and filename of a json file that contains the required
                properties on how to clean up the input file.
            output_filename (str): complete path and filename to be generated after cleaning (also in csv format)
        Returns:
            (csv file) the cleaned dataset in csv format
        Raises:
            No exception is raised.
        """
        try:
            # Get the settings for automatic cleaning
            self.__read_cleaning_settings(setup_cleaning_filename)

            # Print info
            print("Reading csv file from " + input_filename, file=sys.stdout)

            df = pd.read_csv(
                input_filename,
                sep=self._setup_dict_file_processing["csv_file_sep"],
                encoding=self._setup_dict_file_processing["csv_file_encoding"],
                dtype=str,
            )

            # Execute automatic cleaning
            df_cleaned = self.__execute_auto_cleaning(df)

            # Print info
            print("Saving csv output file at " + output_filename, file=sys.stdout)

            # Save results to csv file
            df_cleaned.to_csv(
                output_filename,
                sep=self._setup_dict_file_processing["csv_file_sep"],
                encoding=self._setup_dict_file_processing["csv_file_encoding"],
                index=False,
                header=True,
            )
            return True
        except Exception as e:
            # Print error
            print("Error " + repr(e) + " ocurred", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return False

    def clean_df(self, df, setup_cleaning_filename):
        """
        Cleans up a pandas dataframe and returns another dataframe as result of the cleaning process

        Parameters:
            df (pandas dataframe): dataframe to be cleaned
            setup_cleaning_filename (str): complete path and filename of a json file that contains the required
                properties on how to clean up the input file.
        Returns:
            (pandas dataframe) the cleaned dataframe
        Raises:
            No exception is raised.
        """
        try:
            # Get the settings for automatic cleaning
            self.__read_cleaning_settings(setup_cleaning_filename)

            # Execute automatic cleaning
            df_cleaned = self.__execute_auto_cleaning(df)
            return df_cleaned
        except Exception as e:
            # Print error
            print("Error " + repr(e) + " ocurred", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return None
