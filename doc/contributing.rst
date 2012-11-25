Contributing
============

Here are the steps needed to set up a development and testing environment.

Create a development environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The development environment is created in a virtualenv. The environment
creation requires the *make* and *virtualenv* programs to be installed.

To install *make* under Debian/Ubuntu::

    $ sudo apt-get install build-essential

Under Mac OS/X, *make* is available as part of XCode.

To install virtualenv::

    $ sudo pip install virtualenv

At this point, from the root of this branch, run the command::

    $ make develop

This command will create a ``.venv`` directory in the branch root, ignored
by DVCSes, containing the development virtual environment with all the
dependencies.

Testing and debugging
~~~~~~~~~~~~~~~~~~~~~

Run the tests::

    $ make test

The test suite requires Python >= 2.7, and < 3.x.

Run the tests and lint checks::

    $ make check

Note that the last command also lints the code. To be able to do that,
install the *pocket-lint* package, e.g.::

    $ sudo apt-get install python-pocket-lint

Integration tests are also available. They use Selenium and require Firefox
to be installed. To run all the tests, including integration ones::

    $ make testall

Run the Django shell (Python interpreter)::

    $ make shell

Run the Django development server for manual testing::

    $ make server

See all the available make targets, including info on how to create a Python 3
development environment::

    $ make

Thanks for contributing, and have fun!
