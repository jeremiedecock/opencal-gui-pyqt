===========
OpenCAL GUI
===========

Copyright (c) 2019 Jérémie DECOCK (www.jdhp.org)

* Web site: http://www.jdhp.org/software_en.html#opcgui
* Online documentation: https://jdhp.gitlab.io/opcgui
* Examples: https://jdhp.gitlab.io/opcgui/gallery/

* Notebooks: https://gitlab.com/jdhp/opencal-gui-pyqt-notebooks
* Source code: https://gitlab.com/jdhp/opencal-gui-pyqt
* Issue tracker: https://gitlab.com/jdhp/opencal-gui-pyqt/issues
* OpenCAL GUI on PyPI: https://pypi.org/project/opcgui
* OpenCAL GUI on Anaconda Cloud: https://anaconda.org/jdhp/opcgui


Description
===========

Opencal Python GUI

Note:

    This project is still in beta stage, so the API is not finalized yet.


Dependencies
============

C.f. requirements.txt


.. _install:

Installation (development environment)
======================================

Posix (Linux, MacOSX, WSL, ...)
-------------------------------

From the OpenCAL GUI source code::

    conda deactivate         # Only if you use Anaconda...
    python3 -m venv env
    source env/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements-dev.txt


Windows
-------

From the OpenCAL GUI source code::

    conda deactivate         # Only if you use Anaconda...
    python3 -m venv env
    env\Scripts\activate.bat
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements-dev.txt


Installation (production environment)
=====================================

::

    python3 -m pip install opcgui


Documentation
=============

* Online documentation: https://jdhp.gitlab.io/opcgui
* API documentation: https://jdhp.gitlab.io/opcgui/api.html


Example usage
=============

TODO


Troublshooting
==============

https://forum.qt.io/topic/93247/qt-qpa-plugin-could-not-load-the-qt-platform-plugin-xcb-in-even-though-it-was-found/16
apt install libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 


Bug reports
===========

To search for bugs or report them, please use the OpenCAL GUI Bug Tracker at:

    https://gitlab.com/jdhp/opencal-gui-pyqt/issues


License
=======

This project is provided under the terms and conditions of the `MIT License`_.


.. _MIT License: http://opensource.org/licenses/MIT
.. _command prompt: https://en.wikipedia.org/wiki/Cmd.exe
