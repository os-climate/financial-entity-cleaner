import unittest

from financial_entity_cleaner.id_cleaner import banking_id
from financial_entity_cleaner.utils import utils
from tests import test_data_reader

# Test data from csv excel files
# - column_0: official id to be validated
# - column_1: type official id ('isin', 'lei', 'sedol', 'other')
# - column_2: expected result from validation (True, False, NotImplemented)
test_data_filename = "./data/test_cleaner_ids.csv"

# Data for processing as lists
test_ids_rows = []


# Load tests data from excel files
def load_test_data():
    global test_ids_rows

    # Read input and output data files
    test_data_reader.read_test_file(test_data_filename, test_ids_rows)
    print("Test data loaded from {}".format(test_data_filename))


class TestOfficialIdCleaner(unittest.TestCase):
    """
    This is the TestCase class that validates official identifiers used in the
    banking industry.
    """

    # Class level setup function, executed once and before any tests function
    @classmethod
    def setUpClass(cls):
        load_test_data()

    # Validate country's info
    def test_validate_ids(self):
        total_rows = len(test_ids_rows)
        print("Total cases to tests {}".format(total_rows))
        # Setup the banking id cleaner and its properties
        banking_id_cleaner = banking_id.BankingIdCleaner()
        banking_id_cleaner.mode = banking_id_cleaner.mode.SILENT_MODE
        banking_id_cleaner.lettercase_output = utils.LOWER_LETTER_CASE
        for data in test_ids_rows:
            # The first column is the input data
            id_to_validate = data[0].strip().lower()

            # The second column is the type of the identifier to be validate
            id_type_to_validate = data[1].strip().lower()

            # The third column is the expected result
            expected_result = eval(data[2].strip())

            print('Testing {}-{}-{}'.format(id_to_validate, id_type_to_validate, expected_result))

            # Validate the ids
            banking_id_cleaner.id_type = id_type_to_validate
            result_validation = banking_id_cleaner.is_valid_id(id_to_validate)
            self.assertEqual(result_validation, expected_result)


def build_test_suite():
    # Create a pool of tests
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestOfficialIdCleaner("test_validate_ids"))
    return test_suite


def build_text_report():
    # Generate a tests report
    test_suite = build_test_suite()
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)


if __name__ == "__main__":
    build_text_report()
