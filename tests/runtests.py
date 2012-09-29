#!/usr/bin/env python

import os
import sys


sys.path.append('..')
backup = os.environ.get('DJANGO_SETTINGS_MODULE', '')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django_nose import NoseTestSuiteRunner


if __name__ == '__main__':
    # Use setup.cfg from current directory.
    os.chdir(os.path.dirname(__file__))
    # Output test names instead of dots.
    runner = NoseTestSuiteRunner(verbosity=2)
    failures = runner.run_tests(['endless_pagination'])
    os.environ['DJANGO_SETTINGS_MODULE'] = backup
    if failures:
        sys.exit(failures)
