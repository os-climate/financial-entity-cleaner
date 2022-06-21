Country's Cleaner
==================================

**Package path: financial\_entity\_cleaner.country**

.. automodule:: financial_entity_cleaner.country

.. toctree::
    :maxdepth: 2

country.iso3166
---------------------------------------------------

.. automodule:: financial_entity_cleaner.country.iso3166
   :members:
   :undoc-members:
   :show-inheritance:

country.exceptions
---------------------------------------------------

.. automodule:: financial_entity_cleaner.country.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

country_cleaner in .json
---------------------------------------------------
This section describes how to customize a .json file to perform automatic/batch processing for normalization of country
information. Check on :doc:`financial_entity_cleaner.auto_cleaner` to understand more about the overall structure of a
.json file that performs multiple cleaning, normalization and validation tasks.

The automatic/batch normalization of country data from a .csv file requires to create a .json file that constains
specific instructions on how to perform the cleaning on country attributes. These instructions are identified by the
key **"country_cleaner"** and its sub-keys, as shown in the example below:

.. code-block:: text

    {
      "file_processing": {
        "csv_file_encoding": "utf-8",
        "csv_file_sep": ","
      },
      "country_cleaner": {
        "input_countries": ["COUNTRY"],
        "name_suffix_clean": "NAME_CLEAN",
        "alpha2_suffix_clean": "ALPHA2_CLEAN",
        "alpha3_suffix_clean": "ALPHA3_CLEAN",
        "output_letter_case": "upper"
      }
    }

The key **"file_processing"** contains a dictionary to inform that the .csv file is encoded in "utf-8" standard and its
attributes are separated by commas. Also, the file has only one country attribute to be normalized that is defined by
the **"input_countries"** key of the **"country_cleaner"** dictionary. Because the CountryCleaner() creates new
attributes, it is necessary to provide suffixes for the normalized name (**name_suffix_clean**), alpha2
(**alpha2_suffix_clean**) and alpha3 (**alpha3_suffix_clean**) so it's possible to differentiate the new fields
from the original ones. The instructions above specify that three new attributes will be added and are named as:
COUNTRY_NAME_CLEAN, COUNTRY_ALPHA2_CLEAN and COUNTRY_ALPHA3_CLEAN. Finally, the **"output_letter_case"** key ensures
that all normalized country information are generated in upper case.

Check the table below for more details and be aware that **all** these keys must be provided as part of the
**"country_cleaner"** dictionary. Otherwise, the automatic/batch cleaning will fail.

.. list-table:: JSON keys to normalize country data
   :widths: 30 10 80
   :header-rows: 1

   * - Key
     - Type
     - Description
   * - input_countries
     - List
     - Name of country attributes in the .csv file to be normalized
   * - name_suffix_clean
     - String
     - Suffix to compose the output country's name
   * - alpha2_suffix_clean
     - String
     - Suffix to compose the output country's alpha2 code
   * - alpha3_suffix_clean
     - String
     - Suffix to compose the output country's alpha3 code
   * - output_letter_case
     - String
     - Output letter case ("lower", "upper" or "title")