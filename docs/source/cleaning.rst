Data Cleaning
========================================

**Data cleaning** or cleasing can be defined as the process of preparing data for analysis by removing or modifying
information that is incorrect, incomplete, irrelevant, duplicated, or improperly formatted. It is a task that aims at
increasing data quality by applying rules to guarantee some level of standardization and well-formatted information.

The **Financial-Entity-Cleaner** provides the four types of cleaning/data normalization tools as listed below:

1) Cleaner for text data based on regex rules
2) Cleaner for company's name with normalization of legal terms
3) Normalization of country information according to ISO 3166-1
4) Validation/Cleaner of banking ID's

Don't hesitate to check our :doc:`tutorials <tutorials>` for some hands-on practice on these topics using jupyter notebooks.

1) Cleaner for text data using regex
---------------------------------------

**Regular expressions** (regex) are sequences of chacteres that specify a search pattern used to "find and replace"
undesirable information on texts. The Financial-Entity-Cleaner provides 26 pre-defined regex rules that can be used
to clean up text information (see table below). Be aware that this cleaning process remove or replace all the
ocurrencies found by the regex pattern, not only the first one. Additionally, the user can also add new rules which can
be executed before or after the pre-defined ones.

.. list-table::
   :widths: 50 100
   :header-rows: 1

   * - Key
     - Description
   * - remove_email
     - Remove e-mails from the text
   * - remove_url
     - Remove URLs from the text. The URL can be http:// or https://
   * - remove_word_the_from_the_end
     - Remove the word THE if it appears in the end of the text
   * - place_word_the_at_the_beginning
     - Add the word THE in the beginning of the text. Used in conjunction with "remove_word_the_from_the_end"
   * - remove_www_address
     - Remove web addresses starting with WWW
   * - enforce_single_space_between_words
     - Remove double spaces from the text
   * - replace_amperstand_by_AND
     - Replace the symbol & with the word AND
   * - replace_hyphen_by_space
     - Replace hyphens (-) with a single space
   * - replace_hyphen_between_spaces_by_single_space
     - Replace hyphens ( - ) with a single space only if it appears between spaces
   * - replace_underscore_by_space
     - Replace underscore symbols (_) with a single space
   * - replace_underscore_between_spaces_by_single_space
     - Replace underscore symbols ( _ ) with a single space only if it appears between spaces
   * - remove_all_punctuation
     - Remove all punctuation symbols
   * - remove_punctuation_except_dot
     - Remove punctuation symbols except for the dot symbol (.)
   * - remove_mentions
     - Remove mentions such as @something
   * - remove_hashtags
     - Remove hashtags (#)
   * - remove_numbers
     - Remove all numbers
   * - remove_text_puctuation
     - Remove text punctuations from text
   * - remove_text_puctuation_except_dot
     - Remove text punctuations from text except the dot symbol (.)
   * - remove_math_symbols
     - Remove math symbols
   * - remove_math_symbols_except_dash
     - Remove math symbols except for the dash symbol (-)
   * - remove_parentheses
     - Remove parentheses ()
   * - remove_brackets
     - Remove brackets []
   * - remove_curly_brackets
     - Remove curly brackets {}
   * - remove_single_quote_next_character
     - Remove single quotes if they appear next to a letter (e.g. a')
   * - remove_words_in_parentheses
     - Remove words that appears between parentheses: (text)
   * - repeat_remove_words_in_parentheses
     - Remove words that appears between two parentheses: ((text))

2) Cleaner for Company's name
--------------------------------

The cleaning process for company's name is a special case of text cleasing and it is treated separated due to its
importance in the OS-Climate context, specially for the purpose of matching corporations described by name in
multiples open data sources (see `Entity-Matching <https://github.com/os-climate/esg-matching>`_ project).

The Financial-Entity-Cleaning library provides a cleaning process for company's name in two levels:

a) Level 1: application of some cleaning rules and
b) Level 2: normalization of company's legal term.

The cleaning rules were described previously in this section and require the user to choose a list of pre-defined or
customized regex to apply. This step removes and/or replace unwanted text from the company's name.

As for the second cleaning level,  the library transcribes any abbreviation of legal terms in the end of the company's
name replacing it for its full legal definition. Therefore, companies in the US legaly defined as LTD, LTD., L.T.D
will be transcribed as LIMITED. Because legal terms are defined by country and it is language-dependent, the library
requires the user to specify the country to be considered when trying to translate the legal term.

.. note:: Currently, the library is capable of recognizing legal terms from **12 countries: Argentina, Brazil, Canada,
   France, Germany, Italy, New Zealand, Portugal, Spain, USA and UK**. If no country is provided, USA legal terms are
   used by default.

The table below illustrates the importance of transcribing legal terms instead of just removing them. Without the full
transcription, these three companies can be considered the same. However, by adding the legal terms transcribed to their
country language, it becomes clear that not only the coporations differ greatly, but are also regulated under specific
country jurisdiction. Such information can be quite usefull, for instance, in the context of entity matching/comparison
and data analysis of companies profile.

.. list-table::
   :widths: 30 10 100
   :header-rows: 1

   * - Original Name
     - Country
     - Clean Name
   * - Analytics Consulting SARL
     - France
     - Analytics Consulting Société à Responsabilité Limitée
   * - Analytics Consulting Ltd.
     - England
     - Analytics Consulting Limited
   * - Analytics Consulting Ltd
     - Portugal
     - Analytics Consulting Limitada

3) Normalization of country
------------------------------

The Financial-Entity-Cleaning library provides normalization of country information according to ISO 3166.
Given a set of country's name, alpha 2, alpha3 codes or a mix of these information, the library searches for the
complete information about the countries. If the search succeeds, the library returns the official names, alpha2 and
alpha3 codes as defined in ISO 3166.

.. note:: If the search is by country name, the library tries to look for the correspondent name using a fuzzy matching
   approach, which enhances the chances of finding a similiar name.

The table below shows some examples:

.. list-table::
   :widths: 15 7 7 15
   :header-rows: 1

   * - Input
     - Alpha2
     - Alpha3
     - Name
   * - France
     - FR
     - FRA
     - France
   * - PT
     - PT
     - PRT
     - Portugal
   * - PER
     - PE
     - PER
     - Peru


4) Validation of banking ID's
-----------------------------

The Financial-Entity-Cleaning library provides validation of banking ID's used in the context of OS-Climate,
such as: ISIN, LEI and SEDOL. The library performs validation on single and multiple ID's, returning if the ID is valid
or not and a cleaning version of the IDs. The cleaning process for these IDs removes unicode characters, punctuation
and spaces. It also returns the IDs in a standardized lower or upper case. The lower case is set by dafault, but users
can change this property, also available to all the other cleaner tools described in this section. The table below
shows some examples of ID validation/cleaning with the cleaning output set to upper case:

.. list-table::
   :widths: 15 7 15 4
   :header-rows: 1

   * - Input
     - Type
     - Clean ID
     - Is Valid
   * - 9695 00 DPKGC9JE9F08 20
     - lei
     - 969500DPKGC9JE9F0820
     - True
   * - sk 1120005824
     - isin
     - SK1120005824
     - False
   * - bfsl3t2
     - sedol
     - BFSL3T2
     - True