"""Settings file for the Django project used for tests."""

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
INSTALLED_APPS = ('endless_pagination',)
ROOT_URLCONF = ''
SITE_ID = 1

# Testing.
NOSE_ARGS = (
    '--verbosity=2',
    '--with-coverage',
    '--cover-package=endless_pagination'
)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
