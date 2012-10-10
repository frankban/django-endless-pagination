"""Endless template tags tests."""

import string
import xml.etree.ElementTree as etree

from django.template import (
    Context,
    Template,
    TemplateSyntaxError,
)
from django.test import TestCase
from django.test.client import RequestFactory

from endless_pagination.exceptions import PaginationError
from endless_pagination.models import PageList
from endless_pagination.settings import (
    PAGE_LABEL,
    PER_PAGE,
)


class TemplateTagsTestMixin(object):
    """Base test mixin for template tags."""

    def setUp(self):
        self.factory = RequestFactory()

    def render(self, request, contents, **kwargs):
        """Render *contents* using given *request*.

        The context data is represented by keyword arguments.
        Is no keyword arguments are provided, a default context will be used.

        Return the generated HTML and the modified context.
        """
        template = Template('{% load endless %}' + contents)
        context_data = kwargs.copy() if kwargs else {'objects': range(47)}
        context_data['request'] = request
        context = Context(context_data)
        html = template.render(context)
        return html.strip(), context

    def request(self, url='/', page=None, data=None, **kwargs):
        """Return a Django request for the given *page*."""
        querydict = {} if data is None else data
        querydict.update(kwargs)
        if page is not None:
            querydict[PAGE_LABEL] = page
        return self.factory.get(url, querydict)


class EtreeTemplateTagsTestMixin(TemplateTagsTestMixin):
    """Mixin for template tags returning a rendered HTML."""

    def render(self, request, contents, **kwargs):
        """Return the etree root node of the HTML output.

        Does not return the context.
        """
        html, _ = super(EtreeTemplateTagsTestMixin, self).render(
            request, contents, **kwargs)
        if html:
            return etree.fromstring('<html>{0}</html>'.format(html))


class PaginateTestMixin(TemplateTagsTestMixin):
    """Test mixin for *paginate* and *lazy_paginate* tags.

    Subclasses must define *tagname*.
    """

    def render(self, request, contents, **kwargs):
        text = string.Template(contents).substitute(tagname=self.tagname)
        return super(PaginateTestMixin, self).render(request, text, **kwargs)

    def test_object_list(self):
        # Ensure the queryset is correctly updated.
        template = '{% $tagname objects %}'
        html, context = self.render(self.request(), template)
        self.assertSequenceEqual(range(PER_PAGE), context['objects'])
        self.assertEqual('', html)

    def test_per_page_argument(self):
        # Ensure the queryset reflects the given ``per_page`` argument.
        template = '{% $tagname 20 objects %}'
        _, context = self.render(self.request(), template)
        self.assertSequenceEqual(range(20), context['objects'])

    def test_per_page_argument_as_variable(self):
        # Ensure the queryset reflects the given ``per_page`` argument.
        # In this case, the argument is provided as context variable.
        template = '{% $tagname per_page entries %}'
        _, context = self.render(
            self.request(), template, entries=range(47), per_page=5)
        self.assertSequenceEqual(range(5), context['entries'])

    def test_first_page_argument(self):
        # Ensure the queryset reflects the given ``first_page`` argument.
        template = '{% $tagname 10,20 objects %}'
        _, context = self.render(self.request(), template)
        self.assertSequenceEqual(range(10), context['objects'])
        # Check the second page.
        _, context = self.render(self.request(page=2), template)
        self.assertSequenceEqual(range(10, 30), context['objects'])

    def test_first_page_argument_as_variable(self):
        # Ensure the queryset reflects the given ``first_page`` argument.
        # In this case, the argument is provided as context variable.
        template = '{% $tagname first_page,subsequent_pages entries %}'
        context_data = {
            'entries': range(47),
            'first_page': 1,
            'subsequent_pages': 40,
        }
        _, context = self.render(self.request(), template, **context_data)
        self.assertSequenceEqual([0], context['entries'])
        # Check the second page.
        _, context = self.render(
            self.request(page=2), template, **context_data)
        self.assertSequenceEqual(range(1, 41), context['entries'])

    def test_starting_from_page_argument(self):
        # Ensure the queryset reflects the given ``starting_from_page`` arg.
        template = '{% $tagname 10 objects starting from page 3 %}'
        _, context = self.render(self.request(), template)
        self.assertSequenceEqual(range(20, 30), context['objects'])

    def test_starting_from_page_argument_as_variable(self):
        # Ensure the queryset reflects the given ``starting_from_page`` arg.
        # In this case, the argument is provided as context variable.
        template = '{% $tagname 10 entries starting from page mypage %}'
        _, context = self.render(
            self.request(), template, entries=range(47), mypage=2)
        self.assertSequenceEqual(range(10, 20), context['entries'])

    def test_using_argument(self):
        # Ensure the template tag uses the given querystring key.
        template = '{% $tagname 20 objects using "my-page" %}'
        _, context = self.render(
            self.request(data={'my-page': 2}), template)
        self.assertSequenceEqual(range(20, 40), context['objects'])

    def test_using_argument_as_variable(self):
        # Ensure the template tag uses the given querystring key.
        # In this case, the argument is provided as context variable.
        template = '{% $tagname 20 entries using qskey %}'
        _, context = self.render(
            self.request(p=3), template, entries=range(47), qskey='p')
        self.assertSequenceEqual(range(40, 47), context['entries'])

    def test_with_argument(self):
        # Ensure the context contains the correct override path.
        template = '{% $tagname 10 objects with "/mypath/" %}'
        _, context = self.render(self.request(), template)
        self.assertEqual('/mypath/', context['endless']['override_path'])

    def test_with_argument_as_variable(self):
        # Ensure the context contains the correct override path.
        # In this case, the argument is provided as context variable.
        path = '/my/path/'
        template = '{% $tagname 10 entries with path %}'
        _, context = self.render(
            self.request(), template, entries=range(47), path=path)
        self.assertEqual(path, context['endless']['override_path'])

    def test_as_argument(self):
        # Ensure it is possible to change the resulting context variable.
        template = '{% $tagname 20 objects as object_list %}'
        _, context = self.render(self.request(), template)
        self.assertSequenceEqual(range(20), context['object_list'])
        # The input queryset has not been changed.
        self.assertSequenceEqual(range(47), context['objects'])

    def test_complete_argument_list(self):
        # Ensure the tag works providing all the arguments.
        template = (
            '{% $tagname 5,10 objects '
            'starting from page 2 '
            'using mypage '
            'with path '
            'as paginated %}'
        )
        _, context = self.render(
            self.request(), template, objects=range(47), mypage='page-number',
            path='mypath')
        self.assertSequenceEqual(range(5, 15), context['paginated'])
        self.assertEqual('mypath', context['endless']['override_path'])

    def test_invalid_arguments(self):
        # An error is raised if invalid arguments are provided.
        templates = (
            '{% $tagname %}',
            '{% $tagname foo bar spam eggs %}',
            '{% $tagname 20 objects as object_list using "mykey" %}',
        )
        request = self.request()
        for template in templates:
            with self.assertRaises(TemplateSyntaxError):
                self.render(request, template)

    def test_invalid_page(self):
        # The first page is displayed if an invalid page is provided.
        template = '{% $tagname 5 objects %}'
        _, context = self.render(self.request(page=0), template)
        self.assertSequenceEqual(range(5), context['objects'])

    def test_nested_context_variable(self):
        # Ensure nested context variables are correctly handled.
        manager = {'all': range(47)}
        template = '{% $tagname 5 manager.all as objects %}'
        _, context = self.render(self.request(), template, manager=manager)
        self.assertSequenceEqual(range(5), context['objects'])

    def test_failing_nested_context_variable(self):
        # An error is raised if a nested context variable is used but no
        # alias is provided.
        manager = {'all': range(47)}
        template = '{% $tagname 5 manager.all %}'
        with self.assertRaises(TemplateSyntaxError) as cm:
            self.render(self.request(), template, manager=manager)
        self.assertIn('manager.all', str(cm.exception))

    def test_multiple_pagination(self):
        # Ensure multiple pagination works correctly.
        template = (
            '{% $tagname 10,20 objects %}'
            '{% $tagname 1 items using items_page %}'
            '{% $tagname 5 entries.all using "entries" as myentries %}'
        )
        _, context = self.render(
            self.request(page=2, entries=3), template,
            objects=range(47), entries={'all': string.letters},
            items=['foo', 'bar'], items_page='p')
        self.assertSequenceEqual(range(10, 30), context['objects'])
        self.assertSequenceEqual(['foo'], context['items'])
        self.assertSequenceEqual(string.letters[10:15], context['myentries'])
        self.assertSequenceEqual(string.letters, context['entries']['all'])


class PaginateTest(PaginateTestMixin, TestCase):

    tagname = 'paginate'


class LazyPaginateTest(PaginateTestMixin, TestCase):

    tagname = 'lazy_paginate'


class ShowMoreTest(EtreeTemplateTagsTestMixin, TestCase):

    def test_first_page_next_url(self):
        # Ensure the link to the next page is correctly generated
        # in the first page.
        template = '{% paginate objects %}{% show_more %}'
        tree = self.render(self.request(), template)
        link = tree.find('.//a[@class="endless_more"]')
        expected = '/?{0}={1}'.format(PAGE_LABEL, 2)
        self.assertEqual(expected, link.attrib['href'])

    def test_page_next_url(self):
        # Ensure the link to the next page is correctly generated.
        template = '{% paginate objects %}{% show_more %}'
        tree = self.render(self.request(page=3), template)
        link = tree.find('.//a[@class="endless_more"]')
        expected = '/?{0}={1}'.format(PAGE_LABEL, 4)
        self.assertEqual(expected, link.attrib['href'])

    def test_last_page(self):
        # Ensure the output for the last page is empty.
        template = '{% paginate 40 objects %}{% show_more %}'
        tree = self.render(self.request(page=2), template)
        self.assertIsNone(tree)

    def test_customized_label(self):
        # Ensure the link to the next page is correctly generated.
        template = '{% paginate objects %}{% show_more "again and again" %}'
        tree = self.render(self.request(), template)
        link = tree.find('.//a[@class="endless_more"]')
        self.assertEqual('again and again', link.text)

    def test_customized_loading(self):
        # Ensure the link to the next page is correctly generated.
        template = '{% paginate objects %}{% show_more "more" "working" %}'
        tree = self.render(self.request(), template)
        loading = tree.find('.//*[@class="endless_loading"]')
        self.assertEqual('working', loading.text)


class GetPagesTest(TemplateTagsTestMixin, TestCase):

    def test_page_list(self):
        # Ensure the page list is correctly included in the context.
        template = '{% paginate objects %}{% get_pages %}'
        html, context = self.render(self.request(), template)
        self.assertEqual('', html)
        self.assertIn('pages', context)
        self.assertIsInstance(context['pages'], PageList)

    def test_different_varname(self):
        # Ensure the page list is correctly included in the context when
        # using a different variable name.
        template = '{% paginate objects %}{% get_pages as page_list %}'
        _, context = self.render(self.request(), template)
        self.assertIn('page_list', context)
        self.assertIsInstance(context['page_list'], PageList)

    def test_page_numbers(self):
        # Ensure the current page in the page list reflects the current
        # page number.
        template = '{% lazy_paginate objects %}{% get_pages %}'
        for page_number in range(1, 5):
            _, context = self.render(self.request(page=page_number), template)
            page = context['pages'].current()
            self.assertEqual(page_number, page.number)

    def test_without_paginate_tag(self):
        # An error is raised if this tag is used before the paginate one.
        template = '{% get_pages %}'
        with self.assertRaises(PaginationError):
            self.render(self.request(), template)

    def test_invalid_arguments(self):
        # An error is raised if invalid arguments are provided.
        template = '{% lazy_paginate objects %}{% get_pages foo bar %}'
        request = self.request()
        with self.assertRaises(TemplateSyntaxError):
            self.render(request, template)


class ShowPagesTest(EtreeTemplateTagsTestMixin, TestCase):

    def test_current_page(self):
        # Ensure the current page in the page list reflects the current
        # page number.
        template = '{% paginate objects %}{% show_pages %}'
        for page_number in range(1, 6):
            tree = self.render(self.request(page=page_number), template)
            current = tree.find('.//*[@class="endless_page_current"]')
            text = ''.join(element.text for element in current)
            self.assertEqual(str(page_number), text)

    def test_links(self):
        # Ensure the correct number of links is always displayed.
        template = '{% paginate objects %}{% show_pages %}'
        for page_number in range(1, 6):
            tree = self.render(self.request(page=page_number), template)
            links = tree.findall('.//a')
            expected = 5 if page_number == 1 or page_number == 5 else 6
            self.assertEqual(expected, len(links))

    def test_without_paginate_tag(self):
        # An error is raised if this tag is used before the paginate one.
        template = '{% show_pages %}'
        with self.assertRaises(PaginationError):
            self.render(self.request(), template)

    def test_invalid_arguments(self):
        # An error is raised if invalid arguments are provided.
        template = '{% lazy_paginate objects %}{% show_pages foo bar %}'
        request = self.request()
        with self.assertRaises(TemplateSyntaxError):
            self.render(request, template)


class ShowCurrentNumberTest(TemplateTagsTestMixin, TestCase):

    def test_current_number(self):
        # Ensure the current number is correctly returned.
        template = '{% show_current_number %}'
        for page_number in range(1, 6):
            html, _ = self.render(self.request(page=page_number), template)
            self.assertEqual(page_number, int(html))

    def test_starting_from_page_argument(self):
        # Ensure the number reflects the given ``starting_from_page`` arg.
        template = '{% show_current_number starting from page 3 %}'
        html, _ = self.render(self.request(), template)
        self.assertEqual(3, int(html))

    def test_starting_from_page_argument_as_variable(self):
        # Ensure the number reflects the given ``starting_from_page`` arg.
        # In this case, the argument is provided as context variable.
        template = '{% show_current_number starting from page mypage %}'
        html, _ = self.render(
            self.request(), template, entries=range(47), mypage=2)
        self.assertEqual(2, int(html))

    def test_using_argument(self):
        # Ensure the template tag uses the given querystring key.
        template = '{% show_current_number using "mypage" %}'
        html, _ = self.render(
            self.request(mypage=2), template)
        self.assertEqual(2, int(html))

    def test_using_argument_as_variable(self):
        # Ensure the template tag uses the given querystring key.
        # In this case, the argument is provided as context variable.
        template = '{% show_current_number using qskey %}'
        html, _ = self.render(
            self.request(p=5), template, entries=range(47), qskey='p')
        self.assertEqual(5, int(html))

    def test_as_argument(self):
        # Ensure it is possible add the page number to context.
        template = '{% show_current_number as page_number %}'
        html, context = self.render(self.request(page=4), template)
        self.assertEqual('', html)
        self.assertIn('page_number', context)
        self.assertEqual(4, context['page_number'])

    def test_complete_argument_list(self):
        # Ensure the tag works providing all the arguments.
        template = (
            '{% show_current_number '
            'starting from page 2 '
            'using mypage '
            'as number %}'
        )
        html, context = self.render(
            self.request(), template, objects=range(47), mypage='page-number')
        self.assertEqual(2, context['number'])

    def test_invalid_arguments(self):
        # An error is raised if invalid arguments are provided.
        templates = (
            '{% show_current_number starting from page %}',
            '{% show_current_number foo bar spam eggs %}',
            '{% show_current_number as number using key %}',
        )
        request = self.request()
        for template in templates:
            with self.assertRaises(TemplateSyntaxError):
                self.render(request, template)
