"""Paginator tests."""

from django.test import TestCase

from endless_pagination import paginator


class DefaultPaginatorTest(TestCase):

    def setUp(self):
        self.per_page = 7
        self.paginator = paginator.DefaultPaginator(
            range(30), self.per_page, orphans=2)

    def test_object_list(self):
        # Ensure the paginator correctly returns objects for each page.
        expected = range(self.per_page, self.per_page * 2)
        object_list = self.paginator.page(2).object_list
        self.assertSequenceEqual(expected, object_list)
