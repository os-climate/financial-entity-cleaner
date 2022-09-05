""" The **text.simple_cleaner** module contains the implementation of the **SimpleCleaner()** class which provides
functions to clean up generic texts, being it a sentence or a set of paragraphs.
"""

import re

import unidecode

from financial_entity_cleaner.utils import BaseCleaner
from financial_entity_cleaner.text import cleaning_rules


class SimpleCleaner(BaseCleaner):
    """
    Class used to clean up strings or entire texts.

    Given any string, this class can apply regex rules or perform operations that cleans up the text.

    The code below shows how to apply SimpleCleaner() on a string passed as parameter to .

    Examples:
        .. code-block:: python

            # Creates a SimpleCleaner() object
            from financial_entity_cleaner.text import SimpleCleaner
            txt_cleaner = SimpleCleaner()
            txt_cleaner.clean('Hello, WOrld!')

    """

    def __init__(self):
        super().__init__()

        self._dict_cleaning_rules = cleaning_rules.cleaning_rules_dict
        self._mode = self.SILENT_MODE
        self._letter_case = self.TITLE_LETTER_CASE

    def show_cleaning_rules(self):
        """
        This method shows all the cleaning rules available for use in the library.

        Parameters:
            No parameters.
        Returns:
            (list) with the cleaning rules available in the library.
        Raises:
            No exception raised.
        """
        return list(self._dict_cleaning_rules.keys())

    @staticmethod
    def remove_unicode(value):
        """
        Removes unicode character that is unreadable when converted to ASCII format.

        Parameters:
            value (str): any string containing unicode characters.

        Returns:
            (str): the corresponding input string without unicode characters.

        """
        # Remove all unicode characters if any
        clean_value = value.encode("ascii", "ignore").decode()
        return clean_value

    @staticmethod
    def remove_extra_spaces(value):
        """
        Removes extra spaces in the beggining, the end and between words.

        Parameters:
            value (str): any string with extra spaces.

        Returns:
            (str): the corresponding input string in which extra spaces are transformed to single spaces.

        """
        # Remove spaces in the beginning and in the end and convert it to lower case
        clean_value = value.strip()

        # Remove excessive spaces in between words
        clean_value = re.sub(r"\s+", " ", clean_value)
        return clean_value

    @staticmethod
    def remove_all_spaces(value):
        """
        Removes all spaces in the value.

        Parameters:
            value (str): any string with extra spaces.

        Returns:
            (str): the corresponding input string without spaces.

        """
        # Remove excessive spaces in between words
        clean_value = re.sub(r"\s", "", value)
        return clean_value

    @staticmethod
    def remove_accents(value):
        """
        Replace accents by non-accent letters.

        Parameters:
            value (str): any string with accents.

        Returns:
            (str): the corresponding input string without accents.

        """
        # remove ascents
        clean_value = unidecode.unidecode(value)
        return clean_value

    def apply_cleaning_rules(self, text, lst_rules):
        # Create the dictionary of rules to apply
        cleaning_dict = {}
        for rule_name in lst_rules:
            cleaning_dict[rule_name] = self._dict_cleaning_rules[rule_name]

        # Apply all the cleaning rules
        clean_text = self._apply_regex_rules(text, cleaning_dict)
        return clean_text

    @staticmethod
    def _apply_regex_rules(str_value, dict_regex_rules):
        """
        Applies several cleaning rules based on a custom dictionary sent by parameter. The dictionary must contain
        cleaning rules written in regex format.

        Parameters:
            str_value (str): any value as string to be cleaned up.
            dict_regex_rules (dict): a dictionary of cleaning rules writen in regex as shown below:\n
                [rule name] : ['replacement', 'regex rule']\n
                Example of a regex rule dictionary: \n
                .. code-block:: text

                   {
                        "remove_email": ["", "[.\w]@[.\w]"],
                        "remove_www_address": ["", "https?://[.\w]{3,}|www.[.\w]{3,}"]
                   }

        Returns:
            (str): the modified/cleaned value.

        """

        clean_value = str_value
        # Iterate through the dictionary and apply each regex rule
        for name_rule, cleaning_rule in dict_regex_rules.items():
            # First element is the replacement
            replacement = cleaning_rule[0]
            # Second element is the regex rule
            regex_rule = cleaning_rule[1]

            # Check if the regex rule is actually a reference to another regex rule.
            # By adding a name of another regex rule in the place of the rule itself allows the execution
            # of a regex rule twice
            if regex_rule in dict_regex_rules.keys():
                replacement = dict_regex_rules[cleaning_rule[1]][0]
                regex_rule = dict_regex_rules[cleaning_rule[1]][1]

            # Make sure to use raw string
            regex_rule = r"{}".format(regex_rule)

            # Threat the special case of the word THE at the end of a text's name
            found_the_word_the = False
            if name_rule == 'place_word_the_at_the_beginning':
                found_the_word_the = re.search(regex_rule, clean_value)

            # Apply the regex rule
            clean_value = re.sub(regex_rule, replacement, clean_value)

            # Adjust the name for the case of rule <place_word_the_at_the_beginning>
            if found_the_word_the:
                clean_value = 'the ' + clean_value

        return clean_value
