Installation
========================================

Dependencies
--------------

No matter the type of installation you choose, the installer will manage all the dependencies so that you are not
required to install them manually. But, for the record the minimal dependencies are:

* python >= 3.6.1 or < 3.11
* numpy >= 1.16.0
* pandas >= 1.1.5
* tqdm >= 4.62.2
* python-stdnum >= 1.17
* hdx-python-country >= 3.0.7


Installation using pip
------------------------

To use the **Financial-Entity-Cleaner library**, simply install it with ``pip install``. This is the recommeded method
for most of users, those who just want to apply the library in their own projects:

.. code:: sh

    pip install financial-entity-cleaner


Installation from source distribution
---------------------------------------

If you are a developer and wants to install the library, be aware that we use poetry to manage dependencies. Therefore,
you should install poetry first and then, ask poetry to install the library for you:

.. code:: sh

    poetry install


If you prefer not to use poetry, you can also install the library using the setup script:

.. code:: sh

    python setup.py install

