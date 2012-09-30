"""Create a development and testing environment using a virtualenv."""

import subprocess
import os


TESTS = os.path.abspath(os.path.dirname(__file__))
REQUIREMENTS = os.path.join(TESTS, 'test-requires.pip')
WITH_VENV = os.path.join(TESTS, 'with_venv.sh')
VENV = os.path.abspath(os.path.join(TESTS, '..', '.venv'))


def call(*args):
    """Simple ``subprocess.call`` wrapper."""
    if subprocess.call(args):
        raise SystemExit('Error running {0}.'.format(args))


def pip_install(*args):
    """Install packages using pip inside the virtualenv."""
    call(WITH_VENV, 'pip', 'install', *args)


if __name__ == '__main__':
    call('virtualenv', VENV)
    pip_install('-r', REQUIREMENTS)
