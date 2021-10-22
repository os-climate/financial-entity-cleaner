""" This module contains the implementation of CompanyNameCleaner class """

# Import python libraries
import re
import os

# Import third-party libraries
import numpy as np

# Import internal libraries
from financial_entity_cleaner.utils import utils
from financial_entity_cleaner.exceptions.exception_handler import ModeOfUse

from financial_entity_cleaner.company_cleaner import cleaning_rules
from financial_entity_cleaner.company_cleaner import exceptions_company as custom_exception


class CompanyNameCleaner:
    """
        Class to normalize/clean up company´s names.

        Attributes:
            _mode (int): defines if the cleaning task should be performed in silent or exception mode.
                         - EXCEPTION_MODE: the library throws exceptions in case of error during cleaning.
                         - SILENT_MODE: the library returns NaN as the result of the cleaning.
            _dict_cleaning_rules (dict): the dictionary of cleaning rules loaded from a json file. The cleaning rules
                        are written in regex format and can be easily updated or incremented by changing the file.
            _default_cleaning_rules (list): a list of cleaning rules to be applied. The dictionary of
                        cleaning rules may contain rules that are not needed. Therefore, the _default_cleaning_rules
                        allows the user to select only the cleaning rules necessary of interest. This list is also
                        read from a json file and can be easily updated by changing the file or setting up the
                        correspondent class property.
            _normalize_legal_terms (bool): a flag to indicate if the cleaning process must normalize
            company's legal terms. e.g. LTD => LIMITED.
            _dict_legal_terms (dict): the entire dictionary of legal terms loaded from a json file. The legal terms
                        can be easily updated or incremented by changing the file.
            _current_dict_legal_terms (dict): a subset of the legal terms dictionary filtered by language and country.
                        This will be the legal term dictionary to be applied during cleaning. The user can call the
                        set_current_legal_term_dict() method to change the dictionary to another language/country.
            _lang_legal_terms (str): the language of the legal term dictionary.
            _country_legal_terms (str): the alpha2 code country of the legal term dictionary.
            _output_lettercase (str): indicates the letter case (lower, by default) as the result of the cleaning
                        Other options are: 'upper' and 'title'.
            _remove_unicode (bool): indicates if the unicode character should be removed or not, which may depend
                        on the language of the company's name.
    """

    # Constants used interally by the class
    __DEFAULT_COUNTRY = 'us'
    __DEFAULT_LANG = 'en'

    __CURRENT_DIR = os.path.dirname(__file__) or '.'
    __CURRENT_MODULE_DIR = os.path.abspath(__CURRENT_DIR)

    __NAME_LEGAL_TERMS_DICT = 'legal_forms.json'
    __NAME_JSON_ENTRY_LEGAL_TERMS = 'legal_forms'

    __AVAILABLE_LEGAL_TERMS_DICT = ["en,us", "pt,pt", "pt,br", "fr,fr"]

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

        # The dictionary of cleaning rules define which regex functions to apply to the data
        # A default set of regex rules is defined, but it can be changed by the user.
        self._dict_cleaning_rules = cleaning_rules.cleaning_rules_dict
        self._default_cleaning_rules = cleaning_rules.default_company_cleaning_rules

        # The dictionary of legal terms define how to normalize the company's legal form abreviations
        # By default, the library is set to normalize the legal terms and to use the us/english dictionary.
        # But, the user can change these settings by defining a new value for language and country or
        # request not to use the normalization at all.
        self._normalize_legal_terms = True      # indicates if legal terms need to be normalized
        self._dict_legal_terms = {}             # the complete dictionary of legal terms from json file
        self._current_dict_legal_terms = {}     # the dictionary to be applied filtered by language/country

        # Load the dictionary of legal terms from json file
        self.__load_legal_terms_dict()

        self._lang_legal_terms = self.__DEFAULT_LANG          # the language of the legal term dict to be used
        self._country_legal_terms = self.__DEFAULT_COUNTRY    # the country of the legal term dict to be used

        # Load the legal term dictionary to be used according to the default language and country
        self.set_current_legal_term_dict(self._lang_legal_terms, self._country_legal_terms)

        # Define the letter case of the cleaning output
        self._output_lettercase = utils.LOWER_LETTER_CASE

        # Define if unicode characters should be removed from company's name
        # This cleaning rule is treated separated from the regex rules because it depends on the
        # language of the company's name. For instance, russian or japanese company's may contain
        # unicode characters, while portuguese and french companies may not.
        self._remove_unicode = False

    # Setters and Getters for the properties, so to allow user to setup the library according to his/her needs.
    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, new_mode):
        self._mode = new_mode

    @property
    def normalize_legal_terms(self):
        return self._normalize_legal_terms

    @normalize_legal_terms.setter
    def normalize_legal_terms(self, new_value):
        self._normalize_legal_terms = new_value

    @property
    def output_lettercase(self):
        return self._output_lettercase

    @output_lettercase.setter
    def output_lettercase(self, new_value):
        self._output_lettercase = new_value

    @property
    def remove_unicode(self):
        return self._remove_unicode

    @remove_unicode.setter
    def remove_unicode(self, new_value):
        self._remove_unicode = new_value

    @property
    def default_cleaning_rules(self):
        return self._default_cleaning_rules

    @default_cleaning_rules.setter
    def default_cleaning_rules(self, list_cleaning_rules):
        # Check if the items in the default list of cleaning rules exist in the dictionary of cleaning rules
        if self.__cleaning_rules_exist_in_dict(list_cleaning_rules):
            self._default_cleaning_rules = list_cleaning_rules
        else:
            raise custom_exception.CleaningRuleNotFoundInTheDictionary

    def __load_legal_terms_dict(self):
        """
        This method loads the dictionary of legal terms that is written in a json file.

        Parameters:
            No parameters are needed.
        Returns:
            No return objects. The dictionary is made available in the class property.
        Raises:
            LegalTermsDictionaryDoesNotExist: if the dictionary does not exist in the module's path
            LegalTermsDictionaryNotFound: if the json file is not formatted correctly and/or there is no
                                          key to identify the dictionary of legal term.
        """
        # Check if the json file for legal terms exists in the module's folder
        path_file_legal_terms = os.path.join(self.__CURRENT_MODULE_DIR, self.__NAME_LEGAL_TERMS_DICT)
        if not os.path.exists(path_file_legal_terms):
            raise custom_exception.LegalTermsDictionaryDoesNotExist

        # Load the legal term dictionary
        dict_json = utils.load_json_file(path_file_legal_terms)

        # Check if there is a json key for the legal terms and load the entire dictionary
        if self.__NAME_JSON_ENTRY_LEGAL_TERMS in dict_json:
            self._dict_legal_terms = dict_json[self.__NAME_JSON_ENTRY_LEGAL_TERMS]
        else:
            raise custom_exception.LegalTermsDictionaryNotFound

    def __cleaning_rules_exist_in_dict(self, list_cleaning_rules):
        """
        This method checks if all the names of cleaning rules informed in a list exist as a
        regex rule in the dictionary of cleaning rules.

        Parameters:
            list_cleaning_rules(list): a list with the names of cleaning rules to be applied
        Returns:
            True: if all the items exist in the dictionary of cleaning rules.
            False: if at least one item does not exist in the in the dictionary of cleaning rules.
        Raises:
            No exception is raised.
        """
        for cleaning_rule in list_cleaning_rules:
            if not (cleaning_rule in self._dict_cleaning_rules):
                return False
        return True

    def get_type_current_legal_term_dict(self):
        """
        This method returns the current language and country of the legal term dictionary in use.

        Parameters:
            No parameters.
        Returns:
            (list) with the language and country of the legal term dictionary.
        Raises:
            No exception raised.
        """
        return [self._lang_legal_terms, self._country_legal_terms]

    def get_types_available_legal_term_dict(self):
        """
        This method returns the types of legal term dictionary available for use in the library.

        Parameters:
            No parameters.
        Returns:
            (list) with the languages/country of the legal term dictionaries available in the library.
        Raises:
            No exception raised.
        """
        return self.__AVAILABLE_LEGAL_TERMS_DICT

    def get_cleaning_rules_available(self):
        """
        This method returns the types of cleaning rules available for use in the library.

        Parameters:
            No parameters.
        Returns:
            (list) with the cleaning rules available in the library.
        Raises:
            No exception raised.
        """
        return list(self._dict_cleaning_rules.keys())

    def set_current_legal_term_dict(self, language, country):
        """
        This method loads/change the current dictionary to be used during cleaning.
        The current dictionary is based on the language and the country informed as parameter.

        Parameters:
            language(str): the language of the legal term dictionary
            country(str): the country of the legal term dictionary (currently using alpha2 code country)
        Returns:
            No return objects. The dictionary is made available in the class property.
        Raises:
            LanguageNotSupported: if the language is not supported by the library
            CountryNotSupported: if the country is not supported by the library
        """
        if language in self._dict_legal_terms:
            lang_dict = self._dict_legal_terms[language]
        else:
            raise custom_exception.LanguageNotSupported

        if country in lang_dict:
            self._current_dict_legal_terms = lang_dict[country]
        else:
            raise custom_exception.CountryNotSupported

        self._lang_legal_terms = language
        self._country_legal_terms = country

    def get_clean_name(self, company_name):
        """
        This method cleans up a company's name.

        Parameters:
            company_name (str): the original company's name
        Returns:
            clean_company_name (str): the clean version of the company's name
        Raises:
            CompanyNameIsNotAString: when [company_name] is not of a string type
        """

        if not isinstance(company_name, str):
            if self._mode == ModeOfUse.EXCEPTION_MODE:
                raise custom_exception.CompanyNameIsNotAString
            else:
                return np.nan

        # Remove all unicode characters in the company's name, if requested
        if self._remove_unicode:
            clean_company_name = utils.remove_unicode(company_name)
        else:
            clean_company_name = company_name

        # Remove space in the beginning and in the end and convert it to lower case
        clean_company_name = clean_company_name.strip().lower()

        # Apply normalization for legal terms
        if self.normalize_legal_terms:
            # Iterate through the dictionary of legal terms
            for replacement, legal_terms in self._current_dict_legal_terms.items():
                # Each replacement has a list of possible terms to be searched for
                replacement = ' ' + replacement.lower() + ' '
                for legal_term in legal_terms:
                    # Make sure to use raw string
                    legal_term = legal_term.lower()
                    # Make sure the legal term is a complete word and it's a raw string
                    legal_term = "\\b" + legal_term + "\\b"
                    regex_rule = r"{}".format(legal_term)
                    # Apply the replacement
                    clean_company_name = re.sub(regex_rule, replacement, clean_company_name)

        # Get the custom dictionary of regex rules to be applied in the cleaning
        cleaning_dict = {}
        for rule_name in self._default_cleaning_rules:
            cleaning_dict[rule_name] = self._dict_cleaning_rules[rule_name]

        # Apply all the cleaning rules
        clean_company_name = utils.apply_regex_rules(clean_company_name, cleaning_dict)

        # Apply the letter case, if different from 'lower'
        if self._output_lettercase == "upper":
            clean_company_name = clean_company_name.upper()
        elif self._output_lettercase == "title":
            clean_company_name = clean_company_name.title()

        # Remove excess of white space that might be introduced during previous cleaning
        clean_company_name = clean_company_name.strip()
        clean_company_name = re.sub(r"\s+", " ", clean_company_name)

        return clean_company_name