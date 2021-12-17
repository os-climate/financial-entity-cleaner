# Import python libraries
import re
import json

# Constants that define the letter case for return strings
LOWER_LETTER_CASE = "lower"
UPPER_LETTER_CASE = "upper"
TITLE_LETTER_CASE = "title"


def perform_basic_cleaning(value):
    # Remove all unicode characters if any
    value = remove_unicode(value)

    # Remove spaces in the beginning and in the end and convert it to lower case
    value = remove_extra_spaces(value)

    return value


def remove_unicode(value):
    """
    Removes unicode character that is unreadable when converted to ASCII format.

    Parameters:
        value (string): any string containing unicode characters
    Returns:
        clean_value (string): a string without unicode characters
    Raises:
        No exception is raised.
    """
    # Remove all unicode characters if any
    clean_value = value.encode("ascii", "ignore").decode()
    return clean_value


def remove_extra_spaces(value):
    """
    Removes extra spaces in the beggining, the end and between words.

    Parameters:
        value (string): any string to clean
    Returns:
        clean_value (string): a string without extra spaces
    Raises:
        No exception is raised.
    """
    # Remove spaces in the beginning and in the end and convert it to lower case
    clean_value = value.strip().lower()

    # Remove excessive spaces in between words
    clean_value = re.sub(r"\s+", " ", clean_value)
    return clean_value


def apply_regex_rules(str_value, dict_regex_rules):
    """
    Applies several cleaning rules based on a custom dictionary sent by parameter.
    The dictionary contains the cleaning rules written in regex.
    See the file cleaning_rules.py in company_cleaner module for an example of a custom cleaning rule dictionary.

    Parameters:
        str_value (str): any name (string) to be cleaned up
        dict_regex_rules (dict): a dictionary of cleaning rules writen in regex
            [rule name] : [two-element list: 'replacement', 'regex rule']
            {'remove_email': ['', '[.\w]@[.\w]'],
             'remove_www_address': ['', 'https?://[.\w]{3,}|www.[.\w]{3,}']}
    Returns:
        clean_value (string): the modified name (string)
    Raises:
        No exception is raised.
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

        # Threat the case of the word THE at the end of a company's name
        found_the_word = False
        if name_rule == 'place_word_the_at_the_beginning':
            found_the_word = re.search(regex_rule, clean_value)

        # Apply the regex rule
        clean_value = re.sub(regex_rule, replacement, clean_value)

        # Adjust the name for the case of rule <place_word_the_at_the_beginning>
        if found_the_word:
            clean_value = 'the ' + clean_value

    return clean_value


def load_json_file(file_to_read):
    """
    Reads a json file and returns its content as a python dictionary.

    Parameters:
        file_to_read (str): complete path and name of a json file
    Returns:
        dict_content (dict): the content of a json file as a python dictionary
    Raises:
        No exception is raised.
    """
    # Reads a json file
    with open(file_to_read, encoding="utf-8") as json_file:
        dict_content = json.load(json_file)
    return dict_content
