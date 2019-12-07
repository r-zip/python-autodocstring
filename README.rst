====================
Python Autodocstring
====================


.. image:: https://img.shields.io/pypi/v/python_autodocstring.svg
        :target: https://pypi.python.org/pypi/python_autodocstring

.. image:: https://img.shields.io/travis/r-zip/python_autodocstring.svg
        :target: https://travis-ci.org/r-zip/python_autodocstring

.. image:: https://readthedocs.org/projects/python-autodocstring/badge/?version=latest
        :target: https://python-autodocstring.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Automatic docstring generation backend for programming editors.


* Free software: MIT license
* Documentation: https://python-autodocstring.readthedocs.io.


Overview
--------

This package was written to fulfill a need: consistent, accurate, and versatile
docstring generation plugins for text editors are difficult to come by. Those
that do work well are usually limited to a single editor ecosystem (e.g.,
`autoDocstring`_).

By providing a backend that can generate docstrings through CLI and JSON-RPC,
this plugin provides functionality that can be used in multiple editors (e.g.,
VSCode, SublimeText, Emacs, and Vim).

Accuracy is ensured by leaning on the excellent `Parso library`_ to perform
round-trip parsing of function arguments, typehints, and raise statements.
Docstring style can be handled by templating on the server side or snippet
expansion of the JSON representation on the client side.

Installion
----------

Since this is a work in progress, install by downloading from GitHub:

.. code-block :: none

   git clone https://github.com/r-zip/python-autodocstring.git

Next, in your virtual environment, run

.. code-block :: none

   cd python-autodocstring && python setup.py


Usage
-----

To use this package from the command line, call :code:`autodocstring` with the
target file and line number:

.. code-block :: none

   autodocstring 'path/to/your/source/file.py' $LINE_NUMBER


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`autoDocstring`: https://github.com/NilsJPWerner/autoDocstring
.. _`Parso library`: https://github.com/davidhalter/parso
