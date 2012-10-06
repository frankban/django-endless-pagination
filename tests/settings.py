"""Settings file for the Django project used for tests."""

import os

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS


PROJECT_NAME = 'project'

# Base paths.
ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT = os.path.join(ROOT, PROJECT_NAME)

# Django configuration.
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
DEBUG = TEMPLATE_DEBUG = True
INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'endless_pagination',
    PROJECT_NAME,
)
ROOT_URLCONF = PROJECT_NAME + '.urls'
SITE_ID = 1
STATIC_ROOT = os.path.join(PROJECT, 'static')
STATIC_URL = '/static/'
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    PROJECT_NAME + '.context_processors.navbar',
    PROJECT_NAME + '.context_processors.versions',
)
TEMPLATE_DIRS = os.path.join(PROJECT, 'templates')

# Testing.
NOSE_ARGS = (
    '--verbosity=2',
    '--with-coverage',
    '--cover-package=endless_pagination'
)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
