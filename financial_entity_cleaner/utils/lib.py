""" The **financial_entity_cleaner.utils.lib** module provides common functions that handle internal aspects of the
library, such as: library's folders and configuration files, logging and progress bars for time-consuming cleaning
processes.
"""

# Import python libs
import os
import sys
import json
import logging
import logging.config
from enum import Enum

# Import third-party libs
from tqdm import tqdm


class ModeOfUse(Enum):
    """
        Controls how to use the library:
        - EXCEPTION_MODE (default): exceptions are triggered whenever something bad is going on
        - SILENT_MODE: no exceptions are triggered, but instead the library returns NAN as result of bad calculations
        This mode can be very useful when running the validator or the cleaner on several entries.
    """
    EXCEPTION_MODE = 1
    SILENT_MODE = 2


LOWER_LETTER_CASE = "lower"
"""
Used to define the property **lettercase_output** that indicates the country information in lower case.

Examples:
    >>> country_cleaner = CountryCleaner()
    >>> country_cleaner.lettercase_output = CountryCleaner.LOWER_LETTER_CASE
"""

UPPER_LETTER_CASE = "upper"
"""
Used to define the property **lettercase_output** that indicates the country information in upper case.

Examples:
    >>> country_cleaner = CountryCleaner()
    >>> country_cleaner.lettercase_output = CountryCleaner.UPPER_LETTER_CASE
"""

TITLE_LETTER_CASE = "title"
"""
Used to define the property **lettercase_output** to indicate the country information with the first letter in 
upper case and the remaining ones in lower case.

Examples:
    >>> country_cleaner = CountryCleaner()
    >>> country_cleaner.lettercase_output = CountryCleaner.TITLE_LETTER_CASE
"""


def get_app_path():
    """
    Gets the library's root directory, where the main() method is defined.

    Returns:
        (str): the absolute path of the library's root directory.
    """

    try:
        root_dir = os.path.abspath(sys.modules['__main__'].__file__)
    except:
        root_dir = sys.executable
    return os.path.dirname(root_dir)


def get_logger():
    """
    Gets the logger object as a way to standardize the output messages generated in the library.
    The logging messages can be directed to the standard output (screen) or to a log file, depending on the
    log configuration available at logger.conf.

    Returns:
        (logging.Logger): a logger object that handles output messages.

    """

    logging.config.fileConfig(fname=os.path.join(get_app_path(), 'logger.conf'), disable_existing_loggers=False)
    logger = logging.getLogger('financial-entity-cleaner')
    return logger


def load_json_file(file_to_read):
    """
    Reads a json file and returns its content as a python dictionary.

    Args:
        file_to_read (str): complete path and name of the json file to read.

    Returns:
        (dict): the content of the json file as a python dictionary.

    Examples:
        >>> json_content = load_json_file('/home/User/Desktop/myjsonfile.json')

    """

    # Reads a json file
    with open(file_to_read, encoding="utf-8") as json_file:
        dict_content = json.load(json_file)
    return dict_content


def get_progress_bar(it_range, total_rows, desc='Wait for cleaning...'):
    """
    Gets a progress bar that counts from the initial value of the iterable object 'range_values' to its end.

    Returns:
        (iterable object): any iterable object.

    """
    # The progress bar will only work if it is relevant (if range_values > 1)
    return tqdm(it_range, total=total_rows,
                disable=total_rows <= 1,
                desc=desc,
                bar_format='{desc}{percentage:3.0f}%|{bar:50}{r_bar}')
