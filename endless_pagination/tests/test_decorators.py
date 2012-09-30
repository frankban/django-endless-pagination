"""Decorator tests."""

from django.test import TestCase
from django.test.client import RequestFactory

from endless_pagination import decorators


class PageTemplateTest(TestCase):

    def setUp(self):
        factory = RequestFactory()

    def test_decorated(self):
        pass


