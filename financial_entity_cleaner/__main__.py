import argparse
import sys

from financial_entity_cleaner.auto_cleaner import auto_cleaner


def read_command_args():
    parser = argparse.ArgumentParser("Read arguments passed via command line")
    parser.add_argument(
        "--json",
        dest="json_filename",
        metavar="L",
        type=str,
        help="filename of json settings",
    )
    parser.add_argument(
        "--in",
        dest="input_filename",
        metavar="L",
        type=str,
        help="input filename to be clean",
    )
    parser.add_argument(
        "--out", dest="output_filename", metavar="L", type=str, help="output filename"
    )
    args = parser.parse_args()
    cleaner_args = {
        "json_filename": args.json_filename,
        "input_filename": args.input_filename,
        "output_filename": args.output_filename,
    }
    if cleaner_args["json_filename"] is None:
        raise Exception('The financial_entity_cleaner from command line requires a json file (cleaning settings)')
    if cleaner_args["input_filename"] is None:
        raise Exception('The financial_entity_cleaner from command line requires an input csv filename')
    if cleaner_args["output_filename"] is None:
        raise Exception('The financial_entity_cleaner from command line requires an output csv filename')
    return cleaner_args


def main():
    # Get the command line arguments
    cleaner_args = read_command_args()

    # Create cleaner object with log directory specified by user or using the default directory
    auto_cleaner_obj = auto_cleaner.AutoCleaner()

    # Perform auto cleaning
    result = auto_cleaner_obj.clean_csv_file(
        cleaner_args["input_filename"],
        cleaner_args["json_filename"],
        cleaner_args["output_filename"]
    )
    if result:
        sys.exit(0)
    else:
        sys.exit("An error ocurred. Check the log application for more details.")


if __name__ == "__main__":
    main()
