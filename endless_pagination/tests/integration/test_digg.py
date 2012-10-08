"""Digg-style pagination integration tests."""

from endless_pagination.tests.integration.base import SeleniumTestCase


class DiggPaginationTest(SeleniumTestCase):

    view_name = 'digg'

    def test_new_elements_loaded(self):
        with self.assertNewElements('object', range(6, 11)):
            self.click_link(2)

    def test_url_not_changed(self):
        with self.assertSameURL():
            self.click_link(2)

    def text_next(self):
        pass

    def text_previous(self):
        pass

    def test_direct_link(self):
        pass
