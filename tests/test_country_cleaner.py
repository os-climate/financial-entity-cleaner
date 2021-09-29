import unittest

from financial_entity_cleaner import country
from tests import test_data_reader

# Test data from csv excel files
# - column_0: country to validate (it can be alpha2, alpha3 or country's name)
# - column_1: expected alpha2 code
# - column_2: expected alpha3 code
# - column_3: expected country name
test_data_filename = "tests/data/test_cleaner_country.csv"

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
    def test_validate_country(self):
        total_rows = len(test_country_rows)
        print("Total cases to tests {}".format(total_rows))
        for data in test_country_rows:
            # The first column is the input data
            country_to_validate = data[0].strip().lower()
            # Remainder columns are the expected values
            expected_alpha2 = data[1].strip().lower()
            expected_alpha3 = data[2].strip().lower()
            expected_name = data[3].strip().lower()
            country_info = country.get_country_info(country_to_validate)
            if expected_alpha2 == "none":
                self.assertIsNone(country_info, "Country was not found")
            else:
                self.assertEqual(country_info["country_alpha2"], expected_alpha2)
                self.assertEqual(country_info["country_alpha3"], expected_alpha3)
                self.assertEqual(country_info["country_name"], expected_name)


def build_test_suite():
    # Create a pool of tests
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestCountryCleaner("test_validate_country"))
    return test_suite


def build_text_report():
    # Generate a tests report
    test_suite = build_test_suite()
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)


if __name__ == "__main__":
    build_text_report()
