"""Endless template tags tests."""

import string

from django.template import (
    Context,
    Template,
    TemplateSyntaxError,
)
from django.test import TestCase
from django.test.client import RequestFactory

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

    def request(self, url='/', page=None, **kwargs):
        """Return a Django request for the given *page*."""
        querydict = kwargs.copy()
        if page is not None:
            querydict[PAGE_LABEL] = page
        return self.factory.get(url, querydict)


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
        html, context = self.render(self.request(), template)
        self.assertSequenceEqual(range(20), context['objects'])

    def test_per_page_argument_as_variable(self):
        # Ensure the queryset reflects the given ``per_page`` argument.
        # In this case, the argument is provided as context variable.
        template = '{% $tagname per_page entries %}'
        html, context = self.render(
            self.request(), template, entries=range(47), per_page=5)
        self.assertSequenceEqual(range(5), context['entries'])

    def test_first_page_argument(self):
        # Ensure the queryset reflects the given ``first_page`` argument.
        template = '{% $tagname 10,20 objects %}'
        html, context = self.render(self.request(), template)
        self.assertSequenceEqual(range(10), context['objects'])
        # Check the second page.
        html, context = self.render(self.request(page=2), template)
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
        html, context = self.render(self.request(), template, **context_data)
        self.assertSequenceEqual([0], context['entries'])
        # Check the second page.
        html, context = self.render(
            self.request(page=2), template, **context_data)
        self.assertSequenceEqual(range(1, 41), context['entries'])

    def test_starting_from_page_argument(self):
        # Ensure the queryset reflects the given ``starting_from_page`` arg.
        template = '{% $tagname 10 objects starting from page 3 %}'
        html, context = self.render(self.request(), template)
        self.assertSequenceEqual(range(20, 30), context['objects'])

    def test_starting_from_page_argument_as_variable(self):
        # Ensure the queryset reflects the given ``starting_from_page`` arg.
        # In this case, the argument is provided as context variable.
        template = '{% $tagname 10 entries starting from page mypage %}'
        html, context = self.render(
            self.request(), template, entries=range(47), mypage=2)
        self.assertSequenceEqual(range(10, 20), context['entries'])

    def test_using_argument(self):
        # Ensure the template tag uses the given querystring key.
        template = '{% $tagname 20 objects using "mypage" %}'
        html, context = self.render(
            self.request(mypage=2), template)
        self.assertSequenceEqual(range(20, 40), context['objects'])

    def test_using_argument_as_variable(self):
        # Ensure the template tag uses the given querystring key.
        # In this case, the argument is provided as context variable.
        template = '{% $tagname 20 entries using qskey %}'
        html, context = self.render(
            self.request(p=3), template, entries=range(47), qskey='p')
        self.assertSequenceEqual(range(40, 47), context['entries'])

    def test_with_argument(self):
        # Ensure the context contains the correct override path.
        template = '{% $tagname 10 objects with "/mypath/" %}'
        html, context = self.render(self.request(), template)
        self.assertEqual('/mypath/', context['endless_override_path'])

    def test_with_argument_as_variable(self):
        # Ensure the context contains the correct override path.
        # In this case, the argument is provided as context variable.
        path = '/my/path/'
        template = '{% $tagname 10 entries with path %}'
        html, context = self.render(
            self.request(), template, entries=range(47), path=path)
        self.assertEqual(path, context['endless_override_path'])

    def test_as_argument(self):
        # Ensure it is possible to change the resulting context variable.
        template = '{% $tagname 20 objects as object_list %}'
        html, context = self.render(self.request(), template)
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
        html, context = self.render(
            self.request(), template, objects=range(47), mypage='page-number',
            path='mypath')
        self.assertSequenceEqual(range(5, 15), context['paginated'])
        self.assertEqual('mypath', context['endless_override_path'])

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


class PaginateTest(PaginateTestMixin, TestCase):

    tagname = 'paginate'


class LazyPaginateTest(PaginateTestMixin, TestCase):

    tagname = 'lazy_paginate'


class ShowMoreTest(TestCase):

    pass


class GetPagesTest(TestCase):

    pass


class ShowPagesTest(TestCase):

    pass


class ShowCurrentNumberTest(TestCase):

    pass

