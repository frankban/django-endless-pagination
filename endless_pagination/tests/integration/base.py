"""Integration tests base objects definitions."""

from contextlib import contextmanager
import os

from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from django.utils import unittest
from selenium.common import exceptions
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import ui


USE_SELENIUM = os.getenv('USE_SELENIUM', False)


@unittest.skipUnless(USE_SELENIUM, 'env variable USE_SELENIUM is not set.')
class SeleniumTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        if USE_SELENIUM:
            cls.selenium = WebDriver()
            cls.wait = ui.WebDriverWait(cls.selenium, 10)
        super(SeleniumTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        if USE_SELENIUM:
            cls.selenium.quit()
        super(SeleniumTestCase, cls).tearDownClass()

    def setUp(self):
        self.selenium.get(self.url)

    def wait_ajax(self):
        def document_ready(driver):
            script = 'return document.readyState === "complete";'
            return driver.execute_script(script)
        self.wait.until(document_ready)
        return self.wait

    @property
    def url(self):
        return self.live_server_url + reverse(self.view_name)

    def click_link(self, text):
        link = self.selenium.find_element_by_link_text(str(text))
        link.click()
        return link

    def get_current_elements(self, class_name, driver=None):
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

    @contextmanager
    def assertNewElements(self, class_name, new_elements):
        def new_elements_loaded(driver):
            elements = self.get_current_elements(class_name, driver=driver)
            return elements == new_elements
        yield
        self.wait_ajax().until(new_elements_loaded)

    @contextmanager
    def assertSameURL(self):
        current_url = self.selenium.current_url
        yield
        self.wait_ajax()
        self.assertEqual(current_url, self.selenium.current_url)
