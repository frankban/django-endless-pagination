"""Create a development and testing environment using a virtualenv."""

from __future__ import unicode_literals
import os
import subprocess
import sys


if sys.version_info[0] >= 3:
    # FIXME: a different requirements file will no longer be required once
    # Django 1.5 is released.
    REQUIREMENTS_FILE = 'test-requires3.pip'
    VENV_NAME = '.venv3'
    # FIXME: running 2to3 on django-nose will no longer be required once
    # the project supports Python 3.
    PATCH_DJANGO_NOSE = True
else:
    REQUIREMENTS_FILE = 'test-requires.pip'
    VENV_NAME = '.venv'
    PATCH_DJANGO_NOSE = False


TESTS = os.path.abspath(os.path.dirname(__file__))
REQUIREMENTS = os.path.join(TESTS, REQUIREMENTS_FILE)
WITH_VENV = os.path.join(TESTS, 'with_venv.sh')
VENV = os.path.abspath(os.path.join(TESTS, '..', VENV_NAME))


def call(*args):
    """Simple ``subprocess.call`` wrapper."""
    if subprocess.call(args):
        raise SystemExit('Error running {0}.'.format(args))


def pip_install(*args):
    """Install packages using pip inside the virtualenv."""
    call(WITH_VENV, VENV_NAME, 'pip', 'install', '--use-mirrors', *args)


def patch_django_nose():
    """Run 2to3 on django-nose and remove ``import new`` from its runner."""
    # FIXME: delete once django-nose supports Python 3.
    python = 'python' + '.'.join(map(str, sys.version_info[:2]))
    django_nose = os.path.join(
        VENV, 'lib', python, 'site-packages', 'django_nose')
    call('2to3', '-w', '--no-diffs', django_nose)
    with open(os.path.join(django_nose, 'runner.py'), 'r+') as f:
        lines = [line for line in f.readlines() if 'import new' not in line]
        f.seek(0)
        f.truncate()
        f.writelines(lines)


if __name__ == '__main__':
    call('virtualenv', '--distribute', '-p', sys.executable, VENV)
    pip_install('-r', REQUIREMENTS)
    # FIXME: delete from now on once django-nose supports Python 3.
    if PATCH_DJANGO_NOSE:
        patch_django_nose()
