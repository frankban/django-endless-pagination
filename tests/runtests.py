#!/usr/bin/env python
import os
import sys

sys.path.append('..')
backup = os.environ.get('DJANGO_SETTINGS_MODULE', '')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

try:
    from django.test.simple import DjangoTestSuiteRunner
except ImportError:
    from django.test.simple import run_tests
else:
    run_tests = DjangoTestSuiteRunner().run_tests

if __name__ == "__main__":
    failures = run_tests(['endless_pagination'])
    if failures:
        sys.exit(failures)
    os.environ['DJANGO_SETTINGS_MODULE'] = backup
