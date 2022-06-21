import unittest
import math

from financial_entity_cleaner.country import iso3166
from financial_entity_cleaner.utils import lib
from tests import test_data_reader

# Test data from csv excel files
# - column_0: country to validate (it can be alpha2, alpha3 or country's name)
# - column_1: expected alpha2 code
# - column_2: expected alpha3 code
# - column_3: expected country name
test_data_filename = "./data/test_cleaner_country.csv"

# Data for processing as lists
test_country_rows = []


# Load tests data from excel files
def load_test_data():
    global test_country_rows

    # Read input and output data files
    test_data_reader.read_test_file(test_data_filename, test_country_rows)
    print("Test data loaded from {}".format(test_data_filename))


class TestCountryCleaner(unittest.TestCase):
    """
    This is the TestCase class that tests cleaning functions for country information.
    """

    # Class level setup function, executed once and before any tests function
    @classmethod
    def setUpClass(cls):
        load_test_data()

    # Validate country's info
    def test_validate_countries(self):
        total_rows = len(test_country_rows)
        print("Total cases to tests {}".format(total_rows))

        # Set up the cleaner and its properties
        country_cleaner = iso3166.CountryCleaner()
        country_cleaner.mode = country_cleaner.mode.SILENT_MODE
        country_cleaner.lettercase_output = lib.LOWER_LETTER_CASE
        country_cleaner.country_name_output = "country_name"
        country_cleaner.country_alpha2_output = "country_alpha2"
        country_cleaner.country_alpha3_output = "country_alpha3"
        for data in test_country_rows:
            # The first column is the input data
            country_to_validate = data[0].strip().lower()
            # Remainder columns are the expected values
            expected_alpha2 = data[1].strip().lower()
            if expected_alpha2 == 'None':
                expected_alpha2 = math.nan
            expected_alpha3 = data[2].strip().lower()
            if expected_alpha3 == 'None':
                expected_alpha3 = math.nan
            expected_name = data[3].strip().lower()
            if expected_name == 'None':
                expected_name = None

            # Validate country info
            country_info = country_cleaner.get_clean_data(country_to_validate)

            # Assert the cleaning process
            print('Testing {}'.format(data))
            if expected_alpha2 == 'none':
                self.assertTrue(country_info is None)
            else:
                self.assertEqual(country_info["iso_alpha2"], expected_alpha2)

            if expected_alpha3 == 'none':
                self.assertTrue(country_info is None)
            else:
                self.assertEqual(country_info["iso_alpha3"], expected_alpha3)

            if expected_name == 'none':
                self.assertTrue(country_info is None)
            else:
                self.assertEqual(country_info["iso_name"], expected_name)


def build_test_suite():
    # Create a pool of tests
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestCountryCleaner("test_validate_countries"))
    return test_suite


def build_text_report():
    # Generate a tests report
    test_suite = build_test_suite()
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)


if __name__ == "__main__":
    build_text_report()
