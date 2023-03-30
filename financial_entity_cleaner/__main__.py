import argparse
import sys

from financial_entity_cleaner.batch import cleaner


def read_command_args():
    parser = argparse.ArgumentParser("Read arguments passed via command line")
    parser.add_argument(
        "--set",
        dest="settings_filename",
        metavar="L",
        type=str,
        help="filename for cleaning settings",
    )
    parser.add_argument(
        "--in",
        dest="input_filename",
        metavar="L",
        type=str,
        help="input filename to be cleaned",
    )
    parser.add_argument(
        "--out", dest="output_filename", metavar="L", type=str, help="output filename"
    )
    args = parser.parse_args()
    cleaner_args = {
        "settings_filename": args.settings_filename,
        "input_filename": args.input_filename,
        "output_filename": args.output_filename,
    }
    if cleaner_args["settings_filename"] is None:
        raise Exception('The financial_entity_cleaner from command line requires a settings file (json or yaml)')
    if cleaner_args["input_filename"] is None:
        raise Exception('The financial_entity_cleaner from command line requires an input csv filename')
    if cleaner_args["output_filename"] is None:
        raise Exception('The financial_entity_cleaner from command line requires an output csv filename')
    return cleaner_args


def main():
    # Get the command line arguments
    cleaner_args = read_command_args()

    # Create cleaner object and set its main properties
    auto_cleaner_obj = cleaner.AutoCleaner()
    auto_cleaner_obj.input_filename = cleaner_args["input_filename"]
    auto_cleaner_obj.output_filename = cleaner_args["output_filename"]
    auto_cleaner_obj.settings_file = cleaner_args["settings_filename"]

    # Perform auto cleaning
    result = auto_cleaner_obj.clean_file()
    if result:
        sys.exit(0)
    else:
        sys.exit("An error ocurred. Check the log application for more details.")


if __name__ == "__main__":
    main()
