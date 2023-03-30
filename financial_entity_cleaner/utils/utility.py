import os
import sys
import json
import glob
import logging
import logging.config
from tqdm import tqdm


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


def get_missing_items(ref_list, target_list):
    """
    Compare two lists and return the elements in the target_list that are not in the ref_list.
    If all elements of the target_list are in ref_list, then return None.

    Args:
        ref_list (list): a list used as reference in the comparison.
        target_list (list): a list that will be compared with the referential one.

    Returns:
        (list or None): return a list with all the missing elements of the target_list that are not in the ref_list.

    Examples:
        >>> my_missing_items = get_missing_items(['apple', 'orange'], ['apple', 'ananas'])

    """

    missing_items = []
    for item in target_list:
        if item not in ref_list:
            missing_items.append(item)

    if len(missing_items) == 0:
        return None

    return missing_items


def get_newest_filename(path, extension_pattern='', filename_pattern=''):
    """
    Retrieves the complete path and name of the newest file on a given folder. Patterns for the name and file extension
    can be provided as filters to better select the files of interest.

    Parameters:
        path (str)
            Complete path of a folder
        extension_pattern (str)
            The file extension used to filter files of interest.
        filename_pattern (str)
            A string pattern that describes a file name and serves as a filter to select the files of interest.

    Returns:
        (bool)
            True if is a folder or False otherwise

    Examples:
        >>> my_folder = '/home/User/Desktop/'
        >>> newest_filename = get_newest_filename(my_folder, '*.csv', 'my_settings_')

    """

    # Normalize path and get all files in the directory
    path = os.path.normpath(path)
    if extension_pattern != '':
        path = "{}{}{}".format(path, os.sep, extension_pattern)
    all_files = glob.glob(path)

    # Create a list of files that follows the filename_pattern
    filtered_files = []
    if filename_pattern != '':
        for file in all_files:
            if str(file).find(filename_pattern) != -1:
                if str(file).find('CLEAN') == -1:
                    filtered_files.append(file)
    else:
        filtered_files = all_files

    if len(filtered_files) == 0:
        return None

    # Get the newest file
    newest_file = max(filtered_files, key=os.path.getctime)
    return newest_file
