from datetime import datetime
import logging
import os
import pandas as pd

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
    __CURRENT_DIR = os.path.dirname(__file__) or '.'
    __CURRENT_MODULE_DIR = os.path.abspath(__CURRENT_DIR)
    __DEFAULT_LOGS_FOLDER = os.path.join(__CURRENT_MODULE_DIR, 'logs')

    # Keys in the json file
    __SETUP_KEY_FILE_PROCESSING = 'file_processing'
    __SETUP_KEY_ATTRIBUTE_PROCESSING = 'attribute_processing'
    __SETUP_KEY_COMPANY_CLEANER = 'company_cleaner'
    __SETUP_KEY_COUNTRY_CLEANER = 'country_cleaner'
    __SETUP_KEY_IDS_CLEANER = 'id_cleaner'

    def __init__(self, log_filename=''):
        """
            Constructor method.

            Parameters:
                log_filename (str): complete path and filename to store the autocleaner logs. This is an optional
                    attribute, therefore if it is not specified a default directory is used instead.
            Returns:
                AutoCleaner (object)
            Raises:
                No exception is raised.
        """
        # Setup logging system
        self._logger = None
        if log_filename == '':
            self._log_filename = self.__DEFAULT_LOGS_FOLDER
        else:
            self._log_filename = log_filename
        self.__configure_logging()

        # Internal dictionaries to store required settings for the cleaners by company's name, country and id
        self._setup_dict_company_cleaner = None
        self._setup_dict_country_cleaner = None
        self._setup_dict_ids_cleaner = None

        # Internal dictionary to store required settings to read and save csv files (input and output)
        self._setup_dict_file_processing = None

        # Internal dictionary to store required settings to process the attributes of the input dataset
        self._setup_dict_attribute_processing = None

    def __configure_logging(self):
        """
            Internal method that prepares a logger object as to write logging errors into a file

            Parameters:
                No parameters.
            Returns:
                No return value.
            Raises:
                No exception is raised.
        """
        current_time = datetime.now()
        log_date_time = current_time.strftime('%d%m%Y_%H%M%S')
        self._logger = logging.getLogger('financial_entity_cleaner_AUTO_CLEANER')
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        self._logger.addHandler(stream_handler)
        if self._log_filename != '':
            print(self._log_filename)
            path_log = os.path.abspath(self._log_filename)
            name_log = 'financial_entity_cleaner_' + log_date_time + '.log'
            filename_log = os.path.join(path_log, name_log)
            file_handler = logging.FileHandler(filename_log)
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)
        self._logger.setLevel(logging.ERROR)

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
        # Logger info
        self._logger.info('Reading json setting from ' + setup_cleaning_filename)

        # Read the json file that contains the parameters for automatic cleaning
        dict_json = utils.load_json_file(setup_cleaning_filename)

        # Check if there is a json key to setup the file processing
        if self.__SETUP_KEY_FILE_PROCESSING in dict_json.keys():
            self._setup_dict_file_processing = dict_json[self.__SETUP_KEY_FILE_PROCESSING]

        # Check if there is a json key to setup the dataset processing
        if self.__SETUP_KEY_ATTRIBUTE_PROCESSING in dict_json.keys():
            self._setup_dict_attribute_processing = dict_json[self.__SETUP_KEY_ATTRIBUTE_PROCESSING]

        # Check if there is a json key to setup the cleaning by company's name
        if self.__SETUP_KEY_COMPANY_CLEANER in dict_json.keys():
            self._setup_dict_company_cleaner = dict_json[self.__SETUP_KEY_COMPANY_CLEANER]

        # Check if there is a json key to setup the cleaning by country
        if self.__SETUP_KEY_COUNTRY_CLEANER in dict_json.keys():
            self._setup_dict_country_cleaner = dict_json[self.__SETUP_KEY_COUNTRY_CLEANER]

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
        # Logger info
        self._logger.info('Execute automatic cleaning by country')

        country_cleaner_obj = country.CountryCleaner()
        country_cleaner_obj.lettercase_output = self._setup_dict_country_cleaner['output_letter_case']
        country_attributes = self._setup_dict_country_cleaner['input_countries']
        for country_attribute in country_attributes:
            # For each country, setup the output name, alpha2 and alpha3 to store the cleaned values
            output_name = country_attribute + '_' + self._setup_dict_country_cleaner['name_suffix_clean']
            country_cleaner_obj.country_name_output = output_name

            output_name = country_attribute + '_' + self._setup_dict_country_cleaner['alpha2_suffix_clean']
            country_cleaner_obj.country_alpha2_output = output_name

            output_name = country_attribute + '_' + self._setup_dict_country_cleaner['alpha3_suffix_clean']
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

        # Logger info
        self._logger.info('Execute automatic cleaning by id')

        id_cleaner_obj = banking_id.BankingIdCleaner()
        id_cleaner_obj.lettercase_output = self._setup_dict_ids_cleaner['output_letter_case']
        ids_attributes = self._setup_dict_ids_cleaner['input_ids']
        out_id_suffix_clean = self._setup_dict_ids_cleaner['id_suffix_clean']
        out_id_suffix_valid = self._setup_dict_ids_cleaner['id_suffix_valid']
        set_null_for_invalid_ids = eval(self._setup_dict_ids_cleaner['set_null_for_invalid_ids'])
        id_cleaner_obj.set_null_for_invalid_ids = set_null_for_invalid_ids
        for id_attribute, id_type in ids_attributes.items():
            id_cleaner_obj.id_type = id_type
            df = id_cleaner_obj.apply_cleaner_to_df(df, id_attribute, out_id_suffix_clean, out_id_suffix_valid)
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

        # Logger info
        self._logger.info('Execute automatic cleaning by company name')

        company_cleaner_obj = company.CompanyNameCleaner()
        company_cleaner_obj.normalize_legal_terms = eval(self._setup_dict_company_cleaner['normalize_legal_terms'])
        company_cleaner_obj.output_lettercase = self._setup_dict_company_cleaner['output_letter_case']
        company_cleaner_obj.remove_unicode = self._setup_dict_company_cleaner['remove_unicode_chars']
        if 'cleaning_rules' in self._setup_dict_company_cleaner:
            cleaning_rules = self._setup_dict_company_cleaner['cleaning_rules']
            company_cleaner_obj.default_cleaning_rules = cleaning_rules
        use_cleaning_country = eval(self._setup_dict_company_cleaner['use_clean_country'])
        if use_cleaning_country:
            country_attribute = self._setup_dict_company_cleaner['input_country']
            input_country = country_attribute + '_' + self._setup_dict_country_cleaner['alpha2_suffix_clean']
        else:
            input_country = self._setup_dict_company_cleaner['input_country']
        input_name = self._setup_dict_company_cleaner['input_company_name']
        output_name = self._setup_dict_company_cleaner['output_company_name']
        merge_legal_terms = eval(self._setup_dict_company_cleaner['merge_legal_terms'])
        df = company_cleaner_obj.apply_cleaner_to_df(df, input_name, output_name, input_country, merge_legal_terms)
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
            # Logger info
            self._logger.info('Selecting and renaming dataset attributes')
            # Get the names of attribute to be selected from the dataset
            attributes_to_read = self._setup_dict_attribute_processing.keys()    # current names
            new_attribute_names = self._setup_dict_attribute_processing.items()  # new names
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

            # Logger info
            self._logger.info('Reading csv file from ' + input_filename)

            df = pd.read_csv(input_filename,
                             sep=self._setup_dict_file_processing['csv_file_sep'],
                             encoding=self._setup_dict_file_processing['csv_file_encoding'])

            # Execute automatic cleaning
            df_cleaned = self.__execute_auto_cleaning(df)

            # Logger info
            self._logger.info('Saving csv file at ' + output_filename)

            # Save results to csv file
            df_cleaned.to_csv(output_filename,
                              sep=self._setup_dict_file_processing['csv_file_sep'],
                              encoding=self._setup_dict_file_processing['csv_file_encoding'],
                              index=False,
                              header=True)
            return True
        except Exception as e:
            # Logger info
            self._logger.error('Error ' + repr(e) + ' ocurred')
            self._logger.error('Error message: ' + str(e))
            print('An error ocurred. Check the log application for more details.')
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
            # Logger info
            self._logger.error('Error ' + repr(e) + ' ocurred')
            self._logger.error('Error message: ' + str(e))
            print('An error ocurred. Check the log application for more details.')
            return None