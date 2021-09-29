from unittest import TestCase, TestSuite, TextTestRunner

from financial_entity_cleaner import company
from tests import test_data_reader

# Test data from csv excel files
# - column_0: company´s name to clean
# - column_1: expected result
test_data_filename = "tests/data/test_cleaner_company.csv"

# Data for processing as lists
test_company_rows = []


# Load tests data from excel files
def load_test_data():
    global test_company_rows

    # Read input and output data files
    test_data_reader.read_test_file(test_data_filename, test_company_rows)
    print("Test data loaded from {}".format(test_data_filename))


class TestCompanyCleaner(TestCase):
    """
    This is the TestCase class for cleaning company's name.
    """

    # Class level setup function, executed once and before any tests function
    @classmethod
    def setUpClass(cls):
        load_test_data()

    # Clean company's name
    def test_clean_company_name(self):
        total_rows = len(test_company_rows)
        print("Total cases to tests {}".format(total_rows))
        print("{:<30} - {:<30} - {:<30}".format("INPUT", "EXPECTED", "OUTPUT"))
        for data in test_company_rows:
            # The first column is the input data
            company_name_to_clean = data[0]

            # The second column is the expected result
            expected_name = data[1].strip().lower()

            # Perform the cleaning
            clean_name = company.get_clean_name(company_name_to_clean)
            print(
                "{:<30} - {:<30} - {:<30}".format(
                    company_name_to_clean, expected_name, clean_name
                )
            )
            self.assertEqual(clean_name, expected_name)


def build_test_suite():
    # Create a pool of tests
    test_suite = TestSuite()
    test_suite.addTest(TestCompanyCleaner("test_clean_company_name"))
    return test_suite


def build_text_report():
    # Generate a tests report
    test_suite = build_test_suite()
    test_runner = TextTestRunner()
    test_runner.run(test_suite)


if __name__ == "__main__":
    build_text_report()
