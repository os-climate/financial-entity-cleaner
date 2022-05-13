Identifier's Cleaner
==================================

**Package path: financial\_entity\_cleaner.id**

.. automodule:: financial_entity_cleaner.id

.. toctree::
    :maxdepth: 2

id.banking
---------------------------------------------------

.. automodule:: financial_entity_cleaner.id.banking
   :members:
   :undoc-members:
   :show-inheritance:

id.exceptions
---------------------------------------------------

.. automodule:: financial_entity_cleaner.id.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

id_cleaner in .json
---------------------------------------------------
This section describes how to customize a .json file to perform automatic/batch processing for validation on ID's.
Check on :doc:`financial_entity_cleaner.auto_cleaner` to understand more about the overall structure of a
.json file that performs multiple cleaning, normalization and validation tasks.

The automatic/batch validation of ID's from a .csv file requires to create a .json file that constains
specific instructions on how to perform this type of cleaning. These instructions are identified by the
key **"id_cleaner"** and its sub-keys, as shown in the example below:

.. code-block:: text

    {
      "file_processing": {
        "csv_file_encoding": "utf-8",
        "csv_file_sep": ","
      },
      "id_cleaner": {
        "input_ids": {
          "ID":  "lei"
        },
        "id_suffix_clean": "CLEAN",
        "id_suffix_valid": "VALID",
        "set_null_for_invalid_ids": "True",
        "output_letter_case": "upper"
      }
    }

The key **"file_processing"** contains a dictionary to inform that the .csv file is encoded in "utf-8" standard and its
attributes are separated by commas. Also, the file has only one ID attribute to be normalized that is defined by
the **"input_ids"** key of the **"id_cleaner"** dictionary. Notice that this key requires to define a dictionary of IDs
in which the *key* is the attribute name in the .csv file and the *value* is the type of the validation. Therefore,
the example above defines validation based on 'lei' for the attribute named 'ID'. Other ID types are 'isin' or 'sedol'.
Because the BankingIdCleaner() creates new attributes, it is necessary to provide suffixes for the cleaned ID
(**id_suffix_clean**) and its validation flag (**id_suffix_valid**) so it's possible to differentiate the new fields
from the original ones. The instructions above specify that two new attributes will be added and are named as:
ID_CLEAN and ID_VALID. Finally, the **"output_letter_case"** key ensures that all cleaned ID's are in upper case.

Check the table below for more details and be aware that **all** these keys must be provided as part of the
**"id_cleaner"** dictionary. Otherwise, the automatic/batch cleaning will fail.

.. list-table:: JSON keys to normalize country data
   :widths: 30 10 80
   :header-rows: 1

   * - Key
     - Type
     - Description
   * - input_ids
     - Dictionary (key=attribute_name; value=ID_type)
     - Attributes in the .csv file that are IDs to be validated
   * - id_suffix_clean
     - String
     - Suffix to compose the output field name for the cleaned ID
   * - id_suffix_valid
     - String
     - Suffix to compose the output field name for the validation flag
   * - set_null_for_invalid_ids
     - String (="True" or "False")
     - Flag to indicate if BankingIdCleaner() returns NaN for invalid ID's
   * - output_letter_case
     - String
     - Output letter case ("lower", "upper" or "title")