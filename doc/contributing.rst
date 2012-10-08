Contributing
============

Steps needed to set up a development and testing environment.

Create a development environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The development environment is created in a virtualenv. The environment
creation requires the *make* and *virtualenv* programs to be installed.

To install *make* under Debian/Ubuntu::

    $ sudo apt-get install build-essential

Under MacOSX, make is available as part of XCode.

To install virtualenv::

    $ sudo pip install virtualenv

At this point, to from the root of this branch, run the command::

    $ make develop

This command will create a ``.venv`` directory in the branch root, ignored
by DVCS, containing the development virtual environment with all the
dependencies.

Testing and debugging
~~~~~~~~~~~~~~~~~~~~~

Run the tests::

    $ make test

Run the tests and lint checks::

    $ make check

Note that the last command also lint the code. To be able to do that,
install the *pocket-lint* package, e.g.::

    $ sudo apt-get install python-pocket-lint

Run the Django shell (Python interpreter)::

    $ make shell

Run the Django development server for manual testing::

    $ make server

Thanks for contributing, and have fun!
