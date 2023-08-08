.. currentmodule:: opcgui

=================
Developer's notes
=================

Getting Started For Developers: set up your package environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

   The following guide is used only if you want to *develop* the
   `opcgui` package. If you just want to write code that uses it
   externally, you should rather install it as explained in the README.rst file.


.. TODO: make a short introduction to explain what is a virtual environment and why it is recommanded to use it

In your terminal, change to the directory where you cloned `opcgui`.

If you use Anaconda, type::

    conda deactivate

Then, if you are on a Posix system (Linux, MacOSX, WSL, ...), type::

    python3 -m venv env
    source env/bin/activate
    pip install --upgrade pip
    pip install -r requirements-dev.txt


If you are in a Windows terminal (for WSL terminal see instructions above), type::

    python3 -m venv env
    env\Scripts\activate.bat
    pip install --upgrade pip
    pip install -r requirements-dev.txt

This will create and activate a Python virtual environment (venv) in the `env` directory.
This virtual environment contains all the opcgui dependencies and a few useful
packages for development and interaction.

You will have to activate the venv any time you open a new
terminal to activate the virtual environment.

* On Windows, in your Anaconda Prompt, run ``source env/bin/activate``
* On MacOSX and Linux, in your Terminal, run ``env\Scripts\activate.bat``

If you want to see the list of packages installed in the virtual environment,
type::

    pip list

If later you want to leave the virtual environment:

* On Windows, in your Anaconda Prompt, run ``deactivate``
* On MacOSX and Linux, in your Terminal, run ``deactivate``

Also if you want to completely remove this environment from your system, you
can simply remove the `env` directory.

See https://docs.python.org/3/library/venv.html for more
information on Python virtual environments.


Bug reports
~~~~~~~~~~~

To search for bugs or report them, please use the Bug Tracker at:

    https://gitlab.com/jdhp/opencal-gui-pyqt/issues

Contribute
~~~~~~~~~~

This project is written for Python 3.x.
Python 2.x is *not* supported.

The `TODO.md`_ file contains the TODO list.

All contributions should at least comply with the following PEPs_:

- PEP8_ "Python's good practices"
- PEP257_ "Docstring Conventions"
- PEP287_ "reStructuredText Docstring Format"

All contribution should be properly documented and tested with unittest_
and/or doctest_.

pylint_, `pep8 <https://github.com/PyCQA/pep8>`__ and pyflakes_ should also be
used to check the quality of each module.

Docstrings should be compatible with the
`Sphinx "napoleon" extension <http://sphinxcontrib-napoleon.readthedocs.org/>`__
and follow the Numpy style:

- `Please follow this guide <https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt>`__
- `Be inspired by these examples <http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html>`__

Changes
~~~~~~~

.. include:: ../CHANGES.rst
   :start-line: 2

.. ......................................................................... ..

.. _MIT license: https://opensource.org/licenses/MIT
.. _available on GitHub: https://gitlab.com/jdhp/opencal-gui-pyqt
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _PEP257: https://www.python.org/dev/peps/pep-0257/
.. _PEP287: https://www.python.org/dev/peps/pep-0287/
.. _PEPs: https://www.python.org/dev/peps/
.. _unittest: https://docs.python.org/3/library/unittest.html
.. _doctest: https://docs.python.org/3/library/doctest.html
.. _pylint: http://www.pylint.org/
.. _pyflakes: https://pypi.python.org/pypi/pyflakes
.. _TODO.md: https://gitlab.com/jdhp/opencal-gui-pyqt/blob/master/TODO.md
