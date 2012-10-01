"""Model tests."""

from contextlib import contextmanager

from django.test import TestCase
from django.test.client import RequestFactory

from endless_pagination import (
    models,
    settings,
)
from endless_pagination.paginator import DefaultPaginator


@contextmanager
def local_settings(**kwargs):
    """Override local Django Endless Pagination settings.

    This context manager can be used in a way similar to Django own
    ``TestCase.settings()``.
    """
    original_values = []
    for key, value in kwargs.items():
        original_values.append([key, getattr(settings, key)])
        setattr(settings, key, value)
    try:
        yield
    finally:
        for key, value in original_values:
            setattr(settings, key, value)


class LocalSettingsTest(TestCase):

    def setUp(self):
        settings._LOCAL_SETTINGS_TEST = 'original'

    def tearDown(self):
        del settings._LOCAL_SETTINGS_TEST

    def test_settings_changed(self):
        # Check that local settings are changed.
        with local_settings(_LOCAL_SETTINGS_TEST='changed'):
            self.assertEqual('changed', settings._LOCAL_SETTINGS_TEST)

    def test_settings_restored(self):
        # Check that local settings are restored.
        with local_settings(_LOCAL_SETTINGS_TEST='changed'):
            pass
        self.assertEqual('original', settings._LOCAL_SETTINGS_TEST)

    def test_restored_after_exception(self):
        # Check that local settings are restored after an exception.
        with self.assertRaises(RuntimeError):
            with local_settings(_LOCAL_SETTINGS_TEST='changed'):
                raise RuntimeError()
            self.assertEqual('original', settings._LOCAL_SETTINGS_TEST)


class PageListTest(TestCase):

    def setUp(self):
        self.paginator = DefaultPaginator(range(30), 7, orphans=2)
        self.current_number = 2
        self.page_label = 'page'
        self.factory = RequestFactory()
        self.request = self.factory.get(
            self.get_path_for_page(self.current_number))
        self.pages = models.PageList(
            self.request, self.paginator.page(self.current_number),
            self.page_label)

    def get_url_for_page(self, number):
        """Return a url for the given page ``number``."""
        return '?{0}={1}'.format(self.page_label, number)

    def get_path_for_page(self, number):
        """Return a path for the given page ``number``."""
        return '/' + self.get_url_for_page(number)

    def check_page(self, page, number, is_first, is_last, is_current):
        """Perform several assertions on the given page attrs."""
        self.assertEqual(number, page.number)
        self.assertEqual(unicode(page.number), page.label)
        self.assertEqual(is_first, page.is_first)
        self.assertEqual(is_last, page.is_last)
        self.assertEqual(is_current, page.is_current)

    def test_length(self):
        # Ensure the length of the page list equals the number of pages.
        self.assertEqual(self.paginator.num_pages, len(self.pages))

    def test_first_page(self):
        # Ensure the attrs of the first page are correctly defined.
        page = self.pages.first()
        self.assertEqual('/', page.path)
        self.assertEqual('', page.url)
        self.check_page(page, 1, True, False, False)

    def test_last_page(self):
        # Ensure the attrs of the last page are correctly defined.
        page = self.pages.last()
        self.check_page(page, len(self.pages), False, True, False)

    def test_current_page(self):
        # Ensure the attrs of the current page are correctly defined.
        page = self.pages.current()
        self.check_page(page, self.current_number, False, False, True)

    def test_path(self):
        # Ensure the path of each page is correctly generated.
        for num, page in enumerate(list(self.pages)[1:]):
            expected = self.get_path_for_page(num + 2)
            self.assertEqual(expected, page.path)

    def test_url(self):
        # Ensure the path of each page is correctly generated.
        for num, page in enumerate(list(self.pages)[1:]):
            expected = self.get_url_for_page(num + 2)
            self.assertEqual(expected, page.url)

    def test_page_render(self):
        # Ensure the page is correctly rendered.
        page = self.pages.first()
        rendered_page = unicode(page)
        self.assertIn('href="/"', rendered_page)
        self.assertIn(page.label, rendered_page)

    def test_current_page_render(self):
        # Ensure the page is correctly rendered.
        page = self.pages.current()
        rendered_page = unicode(page)
        self.assertNotIn('href', rendered_page)
        self.assertIn(page.label, rendered_page)

    def test_page_list_render(self):
        # Ensure the page list is correctly rendered.
        rendered = unicode(self.pages)
        self.assertEqual(5, rendered.count('<a href'))

    def test_page_list_render_just_one_page(self):
        # Ensure nothing is rendered if the page list contains only one page.
        page = DefaultPaginator(range(10), 10).page(1)
        pages = models.PageList(self.request, page, self.page_label)
        self.assertEqual(u'', unicode(pages))

    def test_different_default_number(self):
        # Ensure the page path is generated based on the default number.
        pages = models.PageList(
            self.request, self.paginator.page(2), self.page_label,
            default_number=2)
        self.assertEqual('/', pages.current().path)
        self.assertEqual(self.get_path_for_page(1), pages.first().path)

    def test_index_error(self):
        # Ensure an error if raised if a non existent page is requested.
        with self.assertRaises(IndexError):
            self.pages[len(self.pages) + 1]

    def test_previous(self):
        # Ensure the correct previous page is returned.
        previous_page = self.pages.previous()
        self.assertEqual(self.current_number - 1, previous_page.number)

    def test_next(self):
        # Ensure the correct next page is returned.
        next_page = self.pages.next()
        self.assertEqual(self.current_number + 1, next_page.number)

    def test_no_previous(self):
        # An empty string is returned if the previous page cannot be found.
        pages = models.PageList(
            self.request, self.paginator.page(1), self.page_label)
        self.assertEqual(u'', pages.previous())

    def test_no_next(self):
        # An empty string is returned if the next page cannot be found.
        num_pages = self.paginator.num_pages
        pages = models.PageList(
            self.request, self.paginator.page(num_pages), self.page_label)
        self.assertEqual(u'', pages.next())

    def test_customized_page_list_callable(self):
        # The page list is rendered based on ``settings.PAGE_LIST_CALLABLE``.
        page_list_callable = lambda number, num_pages: [None]
        with local_settings(PAGE_LIST_CALLABLE=page_list_callable):
            rendered = unicode(self.pages).strip()
        expected = u'<span class="endless_separator">...</span>'
        self.assertEqual(expected, rendered)
