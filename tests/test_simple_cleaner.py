import unittest

from tests import test_data_reader
from financial_entity_cleaner import simple_cleaner
from financial_entity_cleaner import cleaner_data

# Test data from csv excel files
# - column_0: name to clean
# - column_1: expected result after cleaning
test_data_filename = "tests/data/test_simple_cleaner.csv"
# test_unicode_filename = 'data/test_cleaner_unicode.csv'

# Data for processing as lists
test_rows = []
test_unicode_rows = []


# Load tests data from excel files
def load_test_data():
    global test_rows
    global test_unicode_rows

    # Read input and output data files
    test_data_reader.read_test_file(test_data_filename, test_rows)
    print("Test data loaded from {}".format(test_data_filename))
    # test_data_reader.read_test_file(test_unicode_filename, test_unicode_rows)
    # print('Test data loaded from {}'.format(test_unicode_filename))


class TestSimpleCleaner(unittest.TestCase):
    """
    This is the TestCase class that tests cleaning functions.
    """

    # Class level setup function, executed once and before any tests function
    @classmethod
    def setUpClass(cls):
        load_test_data()

    # Test removing lettercase and whitespace from names
    def test_simple_cleaning(self):
        total_rows = len(test_rows)
        print("Total cases to tests {}".format(total_rows))
        for data in test_rows:
            # The first column is the input data
            name_to_clean = data[0]

            # The second column is the expected output after cleaning lettercase and whitespace
            expected_name = data[1].strip()
            print("Input {}, Expected {}".format(name_to_clean, expected_name))
            clean_name = simple_cleaner.apply_cleaning_rules(
                name_to_clean, cleaner_data.cleaning_rules_dict
            )
            clean_name = clean_name.title().strip()
            clean_name = clean_name.strip()
            self.assertEqual(clean_name, expected_name)

    # Test removing lettercase and whitespace from names
    def test_remove_unicode(self):
        total_unicode_rows = len(test_unicode_rows)
        print("Total cases to tests {}".format(total_unicode_rows))
        for data in test_unicode_rows:
            # The first column is the input data
            unicode_to_clean = data[0]

            # The second column is the expected output after cleaning lettercase and whitespace
            expected_text = data[1]
            print("Input {}, Expected {}".format(unicode_to_clean, expected_text))
            clean_name = simple_cleaner.clean_unicode(unicode_to_clean)
            self.assertEqual(clean_name, expected_text)


def build_test_suite():
    # Create a pool of tests
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestSimpleCleaner("test_simple_cleaning"))
    # test_suite.addTest(TestSimpleCleaner('test_remove_unicode'))
    return test_suite


def build_text_report():
    # Generate a tests report
    test_suite = build_test_suite()
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)


if __name__ == "__main__":
    build_text_report()
