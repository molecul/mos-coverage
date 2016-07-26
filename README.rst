=================
 Collect coverage tool for MOS 9.x
=================

Setup
-----

First, you need to create a virtual environment on Fuel master and activate it.

::

  $ pip install virtualenv
  $ virtualenv .venv
  $ . .venv/bin/activate
  (.venv)$

Next, install application into the virtual environment.

::

  (.venv)$ pip install -r requirements.txt
  (.venv)$ python setup.py install

Usage
-----

With mos-coverage setup up, you can now use it.

To see a list of commands available, run::

  (.venv)$ moscov --help

Cleaning Up
-----------

Finally, when done, deactivate your virtual environment::

  (.venv)$ deactivate
