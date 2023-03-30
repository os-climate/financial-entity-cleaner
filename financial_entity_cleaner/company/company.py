""" This module contains the implementation of CompanyNameCleaner class """

# Import python libraries
import re
import os
import enum

# Import third-party libraries
import numpy as np

# Import internal libraries
from financial_entity_cleaner.utils.utility import get_progress_bar
from financial_entity_cleaner.utils.utility import load_json_file
from financial_entity_cleaner.utils import BaseCleaner
from financial_entity_cleaner.text import SimpleCleaner

from financial_entity_cleaner.text import cleaning_rules
from financial_entity_cleaner.text import exceptions as simple_cleaner_exceptions
from financial_entity_cleaner.company import _exceptions as custom_exception


class LegalTermLocation(enum.Enum):
    AT_THE_END = 1
    ANYWHERE = 2


class CompanyNameCleaner(BaseCleaner):
    """
    Class to normalize/clean up text´s names.

    Attributes:
        _mode (int): defines if the cleaning task should be performed in silent or exception mode.
                     - EXCEPTION_MODE: the library throws exceptions in case of error during cleaning.
                     - SILENT_MODE: the library returns NaN as the result of the cleaning.
        _default_cleaning_rules (list): a list of cleaning rules to be applied. The dictionary of
                    cleaning rules may contain rules that are not needed. Therefore, the _default_cleaning_rules
                    allows the user to select only the cleaning rules necessary of interest. This list is also
                    read from a json file and can be easily updated by changing the file or setting up the
                    correspondent class property.
        _normalize_legal_terms (bool): a flag to indicate if the cleaning process must normalize
        text's legal terms. e.g. LTD => LIMITED.
        _current_dict_legal_terms (dict): a subset of the legal terms dictionary filtered by language and location.
                    This will be the legal term dictionary to be applied during cleaning. The user can call the
                    set_current_legal_term_dict() method to change the dictionary to another language/location.
        _lang_legal_terms (str): the language of the legal term dictionary.
        _country_legal_terms (str): the alpha2 code location of the legal term dictionary.
        _remove_unicode (bool): indicates if the unicode character should be removed or not, which may depend
                    on the language of the text's name.
    """

    # Constants used interally by the class
    __DEFAULT_COUNTRY = "us"
    __DEFAULT_LANG = "en"

    __CURRENT_DIR = os.path.dirname(__file__) or "."
    __CURRENT_MODULE_DIR = os.path.abspath(__CURRENT_DIR)

    __LEGAL_TERMS_DICT_FOLDER = os.path.join(__CURRENT_MODULE_DIR, "legal_forms")
    __NAME_AVAILABLE_LEGAL_TERMS_DICT_FILE = "available_legal_forms.json"
    __NAME_LEGAL_TERMS_DICT_FILE = "legal_forms.json"
    __NAME_JSON_ENTRY_LEGAL_TERMS = "legal_forms"

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

        super().__init__()

        # The mode property defines if exceptions must be thrown in case of errors
        # EXCEPTION_MODE is useful when debugging or building new applications
        # SILENT_MODE is prefered in production environments
        self._mode = self.SILENT_MODE

        # A default set of regex rules is defined, but it can be changed by the user.
        self._default_cleaning_rules = cleaning_rules.default_company_cleaning_rules

        self._simple_cleaner = SimpleCleaner()

        # The dictionary of legal terms define how to normalize the text's legal form abreviations
        # By default, the library is set to normalize the legal terms and to use the us/english dictionary.
        # But, the user can change these settings by changing the current dictionary (see set_current_legal_term_dict)
        # or by requesting not to use the normalization at all.
        self._normalize_legal_terms = (
            True  # indicates if legal terms need to be normalized
        )
        self._current_dict_legal_terms = (
            {}
        )  # the dictionary to be applied filtered by language/location
        self._default_dict_legal_terms = (
            {}
        )  # the default dictionary of legal terms is the us/english

        # Retrieve the list of current dictionaries available by location and language
        self._legal_terms_available = {}
        self.__load_available_legal_terms_dict()

        # Set the current legal term dictionary as US-ENGLISH
        self._lang_legal_terms = self.__DEFAULT_LANG
        self._country_legal_terms = self.__DEFAULT_COUNTRY
        self.set_current_legal_term_dict(self.__DEFAULT_COUNTRY, self.__DEFAULT_LANG)
        self._default_dict_legal_terms = self._current_dict_legal_terms

        # By default, set the search of legal terms at the end of the text's name
        self._legal_term_location = LegalTermLocation.AT_THE_END

        # Define the letter case of the cleaning output
        self._letter_case = self.LOWER_LETTER_CASE

        # Define if unicode characters should be removed from text's name
        # This cleaning rule is treated separated from the regex rules because it depends on the
        # language of the text's name. For instance, russian or japanese text's may contain
        # unicode characters, while portuguese and french companies may not.
        self._remove_unicode = False

        # Define if the letters with accents are replaced with non-accented ones
        self._remove_accents = False

        # Use space as replacement when applying cleaning rules
        self._space_as_replacement = True

        # Cleaning rules applied in the post-processing
        self._post_cleaning_rules = None

    # Setters and Getters for the properties, so to allow user to setup the library according to his/her needs.
    @property
    def normalize_legal_terms(self):
        return self._normalize_legal_terms

    @normalize_legal_terms.setter
    def normalize_legal_terms(self, new_value):
        self._normalize_legal_terms = new_value

    @property
    def remove_unicode(self):
        return self._remove_unicode

    @remove_unicode.setter
    def remove_unicode(self, new_value):
        self._remove_unicode = new_value

    @property
    def remove_accents(self):
        return self._remove_accents

    @remove_accents.setter
    def remove_accents(self, new_value):
        self._remove_accents = new_value

    @property
    def default_cleaning_rules(self):
        return self._default_cleaning_rules

    @default_cleaning_rules.setter
    def default_cleaning_rules(self, list_cleaning_rules):
        # Check if the items in the default list of cleaning rules exist in the dictionary of cleaning rules
        if cleaning_rules.is_valid(list_cleaning_rules):
            self._default_cleaning_rules = list_cleaning_rules
        else:
            raise simple_cleaner_exceptions.CleaningRuleNotFoundInTheDictionary

    @property
    def post_cleaning_rules(self):
        return self._post_cleaning_rules

    @post_cleaning_rules.setter
    def post_cleaning_rules(self, list_cleaning_rules):
        if list_cleaning_rules is not None:
            # Check if the post-processing list of cleaning rules exist in the dictionary of cleaning rules
            if cleaning_rules.is_valid(list_cleaning_rules):
                self._post_cleaning_rules = list_cleaning_rules
            else:
                raise simple_cleaner_exceptions.CleaningRuleNotFoundInTheDictionary
        else:
            self._post_cleaning_rules = None

    def __load_available_legal_terms_dict(self):
        """
        This method loads a dictionary that describes the legal terms available in the library
        by location and language.

        Parameters:
            No parameters are needed.
        Returns:
            No return objects. The dictionary is made available in the class property.
        Raises:
            ListOfLegalTermsAvailableDoesNotExist: if the file to describe the legal terms available does not exists
            LegalTermsDictionaryNotFound: if the json file is not formatted correctly and/or there is no
                                          key to identify the legal term.
        """

        # Check if the json file for legal terms exists in the module's folder
        path_file_available_legal_terms = os.path.join(
            self.__LEGAL_TERMS_DICT_FOLDER, self.__NAME_AVAILABLE_LEGAL_TERMS_DICT_FILE
        )
        if not os.path.exists(path_file_available_legal_terms):
            raise custom_exception.ListOfLegalTermsAvailableDoesNotExist

        # Load the legal term dictionary
        dict_json = load_json_file(path_file_available_legal_terms)
        self._legal_terms_available = dict_json[self.__NAME_JSON_ENTRY_LEGAL_TERMS]

    def __load_legal_terms_dict(self, country):
        """
        This method loads the dictionary of legal terms that is written in a json file.

        Parameters:
            No parameters are needed.
        Returns:
            No return objects. The dictionary is made available in the class property.
        Raises:
            LegalTermsDictionaryDoesNotExist: if the dictionary does not exist in the module's path
        """

        # Get the filename for the legal term dictionary
        filename_legal_form = country + "_" + self.__NAME_LEGAL_TERMS_DICT_FILE

        # Check if the json file for legal terms exists in the module's folder
        path_file_legal_terms = os.path.join(
            self.__LEGAL_TERMS_DICT_FOLDER, filename_legal_form
        )
        if not os.path.exists(path_file_legal_terms):
            raise custom_exception.LegalTermsDictionaryDoesNotExist

        # Load the legal term dictionary
        dict_json = load_json_file(path_file_legal_terms)

        # Check if there is a json key for the legal terms and load the entire dictionary
        if self.__NAME_JSON_ENTRY_LEGAL_TERMS not in dict_json:
            raise custom_exception.LegalTermsDictionaryNotFound

        # Get the dictionary of legal terms of the specified location
        dict_by_country = dict_json[self.__NAME_JSON_ENTRY_LEGAL_TERMS]

        return dict_by_country

    def get_info_current_legal_term_dict(self):
        """
        This method returns the current language and location of the legal term dictionary in use.

        Parameters:
            No parameters.
        Returns:
            (list) with the language and location of the current legal term dictionary.
        Raises:
            No exception raised.
        """
        return [self._country_legal_terms, self._lang_legal_terms]

    def get_info_default_legal_term_dict(self):
        """
        This method returns the default language and location of the legal term dictionary in use.

        Parameters:
            No parameters.
        Returns:
            (list) with the language and location of the default legal term dictionary.
        Raises:
            No exception raised.
        """
        return [self.__DEFAULT_COUNTRY, self.__DEFAULT_COUNTRY]

    def get_info_available_legal_term_dict(self):
        """
        This method returns the types of legal term dictionary available for use in the library.

        Parameters:
            No parameters.
        Returns:
            (dict) with the location/languages of the legal term dictionaries available in the library.
        Raises:
            No exception raised.
        """
        return self._legal_terms_available

    @staticmethod
    def get_cleaning_rules_available():
        """
        This method returns the types of cleaning rules available for use in the library.

        Parameters:
            No parameters.
        Returns:
            (list) with the cleaning rules available in the library.
        Raises:
            No exception raised.
        """
        return list(cleaning_rules.cleaning_rules_dict.keys())

    def get_current_legal_term_dict(self):
        return self._current_dict_legal_terms

    def reset_default_cleaning_rules(self):
        self._default_cleaning_rules = cleaning_rules.default_company_cleaning_rules

    def set_current_legal_term_dict(
            self, country, language="", merge_legal_terms=False
    ):
        """
        This method loads/change the current dictionary to be used during cleaning.
        The current dictionary is based on the location and language informed as parameter.

        Parameters:
            country(str): the location of the legal term dictionary (currently using alpha2 code location)
            language(str): the language of the legal term dictionary
            merge_legal_terms(bool): the user sets a new dictionary of legal terms by
                specifying the location and language, and additionaly can merge this new dictionary with the one
                defined as default (by standard, the default is us-english)
        Returns:
            No return objects. The dictionary is made available in the class property.
        Raises:
            CountryNotSupported: if the location is not supported by the library
            LanguageNotSupported: if the language is not supported by the library
        """

        # Check if the library supports the legal terms for the specified location
        if country not in self._legal_terms_available.keys():
            raise custom_exception.CountryNotSupported

        # Load the requested legal term dictionary
        dict_country = self.__load_legal_terms_dict(country)

        # If the language is provided, check if there is a legal term disctionary for it
        if language != "":
            if language not in dict_country.keys():
                raise custom_exception.LanguageNotSupported
            else:
                self._current_dict_legal_terms = dict_country[language]
        # If the filter by language is not required, concatenate all the entries in the dictionary
        else:
            concatenated_dict = None
            for lang, dict_legal_term in dict_country.items():
                if concatenated_dict is None:
                    concatenated_dict = dict_legal_term
                else:
                    concatenated_dict.update(dict_legal_term)
            self._current_dict_legal_terms = concatenated_dict

        # Concatenate the new requested dictionary with the default one, if required
        if merge_legal_terms:
            for key, list_legal_terms in self._default_dict_legal_terms.items():
                if key not in self._current_dict_legal_terms.keys():
                    self._current_dict_legal_terms[key] = list_legal_terms

        # Update the language and location
        self._lang_legal_terms = language
        self._country_legal_terms = country

    def _apply_normalization_of_legal_terms(self, company_name):
        # Make sure to remove extra spaces, so legal terms can be found in the end (if requested)
        clean_company_name = company_name.strip()

        # Apply normalization for legal terms
        # Iterate through the dictionary of legal terms
        for replacement, legal_terms in self._current_dict_legal_terms.items():
            # Each replacement has a list of possible terms to be searched for
            replacement = " " + replacement.lower() + " "
            for legal_term in legal_terms:
                # Make sure to use raw string
                legal_term = legal_term.lower()
                # If the legal term has . (dots), then apply regex directly on the legal term
                # Otherwise, if it's a legal term with only letters in sequence, make sure
                # that regex find the legal term as a word (\\bLEGAL_TERM\\b)
                if legal_term.find('.') > -1:
                    legal_term = legal_term.replace(".", "\\.")
                else:
                    legal_term = "\\b" + legal_term + "\\b"
                # Check if the legal term should be found only at the end of the string
                if self._legal_term_location == LegalTermLocation.AT_THE_END:
                    legal_term = legal_term + '$'
                # ...and it's a raw string
                regex_rule = r"{}".format(legal_term)
                # Apply the replacement
                clean_company_name = re.sub(
                    regex_rule, replacement, clean_company_name
                )
        return clean_company_name

    def clean(self, company_name):
        """
        This method cleans up a text's name.

        Parameters:
            company_name (str): the original text's name
        Returns:
            clean_company_name (str): the clean version of the text's name
        Raises:
            CompanyNameIsNotAString: when [company_name] is not of a string type
        """

        if not isinstance(company_name, str):
            if self._mode == self.EXCEPTION_MODE:
                raise custom_exception.CompanyNameIsNotAString
            else:
                return np.nan

        # Remove all unicode characters in the text's name, if requested
        if self._remove_unicode:
            clean_company_name = self._simple_cleaner.remove_unicode(company_name)
        else:
            clean_company_name = company_name

        # Remove space in the beginning and in the end and convert it to lower case
        clean_company_name = clean_company_name.strip().lower()

        # Apply all the pre-processing cleaning rules
        clean_company_name = self._simple_cleaner.apply_cleaning_rules(clean_company_name,
                                                                       self._default_cleaning_rules)

        # Apply normalization for legal terms if required
        if self.normalize_legal_terms:
            clean_company_name = self._apply_normalization_of_legal_terms(clean_company_name)

        # Remove accents if required
        if self._remove_accents:
            clean_company_name = self._simple_cleaner.remove_accents(clean_company_name)

        # Apply the post-processing cleaning rules if required
        if self._post_cleaning_rules is not None:
            # Apply all the post-processing cleaning rules
            clean_company_name = self._simple_cleaner.apply_cleaning_rules(clean_company_name,
                                                                           self._post_cleaning_rules)
        # Apply the letter case, if different from 'lower'
        if self._letter_case == self.UPPER_LETTER_CASE:
            clean_company_name = clean_company_name.upper()
        elif self._letter_case == self.TITLE_LETTER_CASE:
            clean_company_name = clean_company_name.title()

        # Remove excess of white space that might be introduced during previous cleaning
        clean_company_name = self._simple_cleaner.remove_extra_spaces(clean_company_name)

        return clean_company_name

    def clean_df(
            self,
            df,
            in_company_name,
            out_company_name,
            in_country="",
            merge_legal_terms=True,
    ):
        """
        This method cleans up all text's names in a dataframe by selecting the correspondent dictionary of
        legal terms according to a location attribute in that dataframe.

        Parameters:
            df (dataframe): the input dataframe that contains the text's name to be cleaned
            in_company_name (str): the attribute in the dataframe for text's name
            out_company_name (str): the attribute to be created for the clean version of the text's name
            in_country (str): the attribute in the dataframe that indicates the location, which will serve as
                a filter to select the appropriated legal terms dictionary.
            merge_legal_terms(bool): this flag indicates if the default dictionary
                of legal terms should be merged to the new dictionary by coutry,
                defined as default (by standard, the default is us-english)
        Returns:
            df (dataframe): the clean version of the input dataframe
        Raises:
            CompanyNameNotFoundInDataFrame: when [in_company_name_attribute] is not a dataframe's attribute
            CountryNotFoundInDataFrame: when [in_country_attribute] is informed and is not a dataframe's attribute
        """

        # Check if the company_name attribute exists in the dataframe
        if in_company_name not in df.columns:
            raise custom_exception.CompanyNameNotFoundInDataFrame

        # Keep the current legal term dictionary in order to restore it after finishing
        initial_dict_legal_terms = self._current_dict_legal_terms

        # Check if the location attribute exists in the dataframe
        if in_country != "" and in_country not in df.columns:
            raise custom_exception.CountryNotFoundInDataFrame

        # Make a copy so not to change the original dataframe
        new_df = df.copy()

        # Creates the new output attribute that will have the clean version of the text's name
        new_df[out_company_name] = np.nan
        # If the location attribute is provided, iterate over all the countries available in the dataframe
        # as to select the related legal term dictionary
        if in_country != "":
            # Get all the countries available in the dataframe
            countries_in_df = list(new_df[in_country].unique())

            # Get the progress bar based on the dataframe rows
            pg_bar = get_progress_bar(it_range=countries_in_df,
                                      total_rows=len(countries_in_df),
                                      desc='Cleaning company name...')
            for country in pg_bar:
                # By default, if the legal term dictionary for that location is not available,  the library
                # uses the default dictionary (initially set up as to be us-english)
                if str(country).lower() not in self._legal_terms_available.keys():
                    self._current_dict_legal_terms = self._default_dict_legal_terms
                else:
                    self.set_current_legal_term_dict(str(country).lower(), "", merge_legal_terms)
                # Filter the dataframe for that location and apply the cleaning
                if str(country) == 'nan':
                    # Case in which the location is null
                    mask = new_df[in_country].isnull()
                else:
                    # Case in which the location was provided
                    mask = new_df[in_country] == country
                new_df.loc[mask, out_company_name] = new_df[mask].apply(lambda line: self.clean(line[in_company_name]),
                                                                        axis=1)
        # If the location is not informed, the library performs the cleaning by using the current legal term
        # dictionary in all entries of the dataframe
        else:
            pg_bar = get_progress_bar(it_range=new_df.iterrows(),
                                      total_rows=new_df.shape[0],
                                      desc='Cleaning company name...')
            for index, row in pg_bar:
                new_df.loc[index, out_company_name] = self.clean(new_df.loc[index, in_company_name])

            # new_df.loc[:, [out_company_name]] = [self.clean(name) for name in new_df[in_company_name]]

        # Return the current dictionary as the one setup before the function call
        self._current_dict_legal_terms = initial_dict_legal_terms
        return new_df