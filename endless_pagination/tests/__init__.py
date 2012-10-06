"""Test model definitions."""

from django.core.management import call_command
from django.db import models


class TestModel(models.Model):
    """A model used in tests."""

    def __unicode__(self):
        return u'TestModel: {0}'.format(self.id)


call_command('syncdb', verbosity=0)
