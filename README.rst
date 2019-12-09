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

Using a backend that can generate docstrings through CLI and JSON-RPC, this
plugin provides functionality that can be used in multiple editors (e.g.,
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

Next, run

.. code-block :: none

   cd python-autodocstring && make init


Usage
-----

To use this package from the command line, call :code:`autodocstring` with the
target file and line number:

.. code-block :: none

   autodocstring 'path/to/your/source/file.py' $LINE_NUMBER

The client-server usage is still in development, but an example is provided in :code:`examples/client.py`.
To run the example, first start the server in one terminal:

.. code-block :: none

   autodocstring start-server

Then send a request in another terminal using the example script:

.. code-block :: none

   python examples/client.py

You should see similar output to the following in your server terminal:

.. code-block :: none

   Received request: {"jsonrpc": "2.0", "method": "get_docstring_info", "params": {"uri": "autodocstring/autodocstring.py", "line": 29}, "id": 1}
   127.0.0.1 - - [09/Dec/2019 12:51:46] "POST / HTTP/1.1" 200 -

And in your client terminal:

.. code-block :: none

   Received result: {'func_name': 'get_toplevel_defs', 'params': [{'name': 'uri', 'annotation': 'str', 'default': None}], 'return_typehint': 'List[ClassOrFunc]', 'raise_types': [], 'id': 'ef72d79d-6107-40c9-b3d9-9edd81a6fe8d'}


Development
-----------

This package is currently under development. An Emacs plugin is planned. Help is
wanted to develop plugins for other editors. If you are interested in developing
a client, please send an email to ryan.z.pilgrim AT gmail.com.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`autoDocstring`: https://github.com/NilsJPWerner/autoDocstring
.. _`Parso library`: https://github.com/davidhalter/parso
