Be Involved
========================================

**Financial-Entity-Cleaner** is available publicly in `this <http://github.com/os-climate/financial-entity-cleaner/>`_
github repository. It is a project developed and maintained by the Entity-Matching group. If you have questions or
are interested to join us, check our mailing list `here <https://lists.os-climate.org/g/EntityMatching>`_. As part
of the open source initiative you can also:

- Try out our :doc:`Tutorials <tutorials>`,
- Consult the :doc:`Code Reference <code>` or
- Download the latest release or clone the repo to contribute with the development.

Development
--------------

Patches may be contributed via pull requests (PR). All changes must pass our automated build script that performs
several checks on the code, for instance: good coding style (`black <https://black.readthedocs.io/>`_)
and import ordering (`isort <https://pycqa.github.io/isort/>`_) are enforced. Therefore, make sure you install black
and isort in your DEV environment:

.. code:: sh

    pip install black isort

To run black in your local machine for all source code:

.. code:: sh

    black .

To run isort in your local machine for all source code:

.. code:: sh

    isort .

Enabling automatic formatting via `pre-commit <https://pre-commit.com/>`_ is recommended:

.. code:: sh

    pip install pre-commit
    pre-commit install

To run all test units provided, install poetry and use it to run our main test script:

.. code:: sh

    pip install poetry
    poetry run test

Documentation
-----------------

This project uses `sphinx <https://www.sphinx-doc.org/>`_ to generate documentation from the source code. The
`docs\source <https://github.com/os-climate/financial-entity-cleaner/tree/main/docs>`_ directory contains the source
the documention source code. Therefore, if you want to generate the documentation in html format in your local machine,
make sure to install sphinx and its html theme and use the docs\source folder to call sphinx-make process:

.. code:: sh

    pip install sphinx sphinx_rtd_theme
    cd .\docs
    .\make html

Pre-releasing
-----------------

Authorized developers can generate pre-releases on the `TestPyPi <https://test.pypi.org/>`_ environment as follows:

- Prepare a signed release commit updating `version` in pyproject.toml
- Tag the commit using `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_ prepended with "v"
- Push the tag

.. code:: sh

    git commit -sm "Release v0.4.1"
    git tag v0.4.1
    git push --follow-tags


Releasing
-----------

Only authorized developers can generate a release on the `PyPi <https://test.pypi.org/>`_ environment as follows:

- Make sure a tested and approaved version was published in the TestPyPi environment.
- Run the 'Create Release' workflow by selecting the tag previously used to publish into the TestPyPi environment.
