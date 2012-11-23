"""Test model definitions."""

from __future__ import unicode_literals

from django.core.management import call_command
from django.db import models

from endless_pagination import utils


class TestModel(models.Model, utils.UnicodeMixin):
    """A model used in tests."""

    def __unicode__(self):
        return 'TestModel: {0}'.format(self.id)


call_command('syncdb', verbosity=0)
