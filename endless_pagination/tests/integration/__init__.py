"""Integration tests base objects definitions."""

from contextlib import contextmanager
import os

from django.core.urlresolvers import reverse
from django.http import QueryDict
from django.test import LiveServerTestCase
from django.utils import unittest
from selenium.common import exceptions
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import ui


USE_SELENIUM = os.getenv('USE_SELENIUM', False)


def setup_package():
    """Set up the Selenium driver once for all tests."""
    if USE_SELENIUM:
        selenium = SeleniumTestCase.selenium = WebDriver()
        SeleniumTestCase.wait = ui.WebDriverWait(selenium, 10)


def teardown_package():
    """Quit the Selenium driver."""
    if USE_SELENIUM:
        SeleniumTestCase.selenium.quit()


@unittest.skipUnless(USE_SELENIUM, 'env variable USE_SELENIUM is not set.')
class SeleniumTestCase(LiveServerTestCase):

    PREVIOUS = '<<'
    NEXT = '>>'
    MORE = 'More results'

    def setUp(self):
        self.url = self.live_server_url + reverse(self.view_name)

    def get(self, url=None, data=None, **kwargs):
        """Load a web page in the current browser session.

        If *url* is None, *self.url* is used.
        The querydict can be expressed providing *data* or *kwargs*.
        """
        if url is None:
            url = self.url
        querydict = QueryDict('', mutable=True)
        if data is not None:
            querydict.update(data)
        querydict.update(kwargs)
        path = '{0}?{1}'.format(url, querydict.urlencode())
        return self.selenium.get(path)

    def wait_ajax(self):
        """Wait for the document to be ready."""
        def document_ready(driver):
            script = """
                return (
                    document.readyState === 'complete' &&
                    jQuery.active === 0
                );
            """
            return driver.execute_script(script)
        self.wait.until(document_ready)
        return self.wait

    def click_link(self, text):
        """Click the link with the given *text*."""
        link = self.selenium.find_element_by_link_text(str(text))
        link.click()
        return link

    def get_current_elements(self, class_name, driver=None):
        """Return the range of current elements as a list of numbers."""
        elements = []
        path = '//div[contains(@class, "{0}")]/h4'.format(class_name)
        if driver is None:
            driver = self.selenium
        for element in driver.find_elements_by_xpath(path):
            #with self.handle_stale():
            elements.append(int(element.text.split()[1]))
        return elements

    @contextmanager
    def handle_stale(self):
        try:
            yield
        except exceptions.StaleElementReferenceException:
            pass

    def assertElements(self, class_name, elements):
        """Assert the current page contains the given *elements*."""
        current_elements = self.get_current_elements(class_name)
        self.assertSequenceEqual(elements, current_elements)

    @contextmanager
    def assertNewElements(self, class_name, new_elements):
        """Fail when new elements are not found in the page."""
        def new_elements_loaded(driver):
            elements = self.get_current_elements(class_name, driver=driver)
            return elements == new_elements
        yield
        self.wait_ajax().until(new_elements_loaded)

    @contextmanager
    def assertSameURL(self):
        """Assert the URL does not change after executing the yield block."""
        current_url = self.selenium.current_url
        yield
        self.wait_ajax()
        self.assertEqual(current_url, self.selenium.current_url)
