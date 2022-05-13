.. financial_entity_cleaner documentation master file, created by
   sphinx-quickstart on Tue Apr 19 11:55:33 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Financial-Entity-Cleaner
============================

|pypi| |license|

.. |pypi| image:: https://img.shields.io/pypi/v/sphinx-codeautolink.svg
   :target: https://pypi.org/project/sphinx-codeautolink
   :alt: PyPI package

.. |license| image:: https://shields.io/badge/license-Apache%202-blue
   :target: https://choosealicense.com/licenses/apache-2.0/
   :alt: License: Apache 2.0

.. toctree::
   :maxdepth: 2
   :hidden:

   project
   dependencies
   cleaning
   how_to
   code
   release_notes
   license

Financial-Entity-Cleaner is an opensource python library, developed by the OS-Climate team, which aim at providing an
efficient and reliable way to perform data cleaning on company names, country information and identifiers used in the
financial sector.

.. seealso:: To know more about the OS-Climate initiative, check out on: https://os-climate.org/

Be involved
-----------------------

Financial-Entity-Cleaner is available publicly in `this <http://github.com/os-climate/financial-entity-cleaner/>`_ github repository.

- Download the latest release or clone the repo to contribute with the development.
- Read the :doc:`How to... <how_to>` guides and the :doc:`Code Reference <code>` to learn more about the library.
- If you have questions, please email the team's mailing list.

Installation
-----------------------

To use the Financial-Entity-Cleaner library, simply install it with ``pip install``:

.. code:: sh

    pip install financial_entity_cleaner

The intaller will manage all dependencies, therefore you are not required to install them manually.
For the record, the minimal dependencies are:

* python >= 3.6.1 or < 3.11 (not tested)
* numpy >= 1.16.0
* pandas >= 1.1.5
* tqdm >= 4.62.2
* python-stdnum >= 1.17
* hdx-python-country >= 3.0.7


Citation
-----------------------

If you use Financial-Entity-Cleaner for an academic publication, please cite this manual as follows:

.. parsed-literal::
   @misc{financial_entity_cleaner-manual,
      author = {OS Climate},
      title = {Financial-Entity-Cleaner Library: Tutorial \& Reference},
      howpublished =  "\\url{http://github.org}",
   }


Acknowledgements
-----------------------
Financial-Entity-Cleaner was developed to provide a standardized and easy way to clean up data processed in the context
of the OS-Climate project which aims to build a data and software platform to boost global capital flows into climate
change mitigation and resilience.

The core of the original library and its main architecture was written and it is maintained by the Data Lab team of
BnP Paribas in Lisbon.

.. figure:: /_static/images/logo_osc_bnp.png
   :figwidth: 449px
   :target: /_static/images/logo_osc_bnp.png
   :align: center

|
|

* :ref:`genindex`
* :ref:`modindex`
