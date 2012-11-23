"""Ephemeral models used to represent a page and a list of pages."""

from __future__ import unicode_literals

from django.template import (
    Context,
    loader,
)
from django.utils.encoding import iri_to_uri

from endless_pagination import (
    loaders,
    settings,
    utils,
)


# Page templates cache.
_template_cache = {}


class EndlessPage(utils.UnicodeMixin):
    """A page link representation.

    Interesting attributes:

        - *self.number*: the page number;
        - *self.label*: the label of the link
          (usually the page number as string);
        - *self.url*: the url of the page (strting with "?");
        - *self.path*: the path of the page;
        - *self.is_current*: return True if page is the current page displayed;
        - *self.is_first*: return True if page is the first page;
        - *self.is_last*:  return True if page is the last page.
    """

    def __init__(
            self, request, number, current_number, total_number,
            querystring_key, label=None, default_number=1, override_path=None):
        self.number = number
        self.label = utils.text(number) if label is None else label
        self.querystring_key = querystring_key

        self.is_current = number == current_number
        self.is_first = number == 1
        self.is_last = number == total_number

        self.url = utils.get_querystring_for_page(
            request, number, self.querystring_key,
            default_number=default_number)
        path = iri_to_uri(override_path or request.path)
        self.path = '{0}{1}'.format(path, self.url)

    def __unicode__(self):
        """Render the page as a link."""
        context_instance = Context({
            'add_nofollow': settings.ADD_NOFOLLOW,
            'page': self,
            'querystring_key': self.querystring_key,
        })
        if self.is_current:
            template_name = 'endless/current_link.html'
        else:
            template_name = 'endless/page_link.html'
        template = _template_cache.setdefault(
            template_name, loader.get_template(template_name))
        return template.render(context_instance)


class PageList(utils.UnicodeMixin):
    """A sequence of endless pages."""

    def __init__(
            self, request, page, querystring_key,
            default_number=None, override_path=None):
        self._request = request
        self._page = page
        if default_number is None:
            self._default_number = 1
        else:
            self._default_number = int(default_number)
        self._querystring_key = querystring_key
        self._override_path = override_path

    def _endless_page(self, number, label=None):
        """Factory function that returns a EndlessPage instance.

        This method works just like a partial constructor.
        """
        return EndlessPage(
            self._request,
            number,
            self._page.number,
            len(self),
            self._querystring_key,
            label=label,
            default_number=self._default_number,
            override_path=self._override_path,
        )

    def __getitem__(self, value):
        # The type conversion is required here because in templates Django
        # performs a dictionary lookup before the attribute lokups
        # (when a dot is encountered).
        try:
            value = int(value)
        except (TypeError, ValueError):
            # A TypeError says to django to continue with an attribute lookup.
            raise TypeError
        if 1 <= value <= len(self):
            return self._endless_page(value)
        raise IndexError('page list index out of range')

    def __len__(self):
        """The length of the sequence is the total number of pages."""
        return self._page.paginator.num_pages

    def __iter__(self):
        """Iterate over all the endless pages (from first to last)."""
        for i in range(len(self)):
            yield self[i + 1]

    def __unicode__(self):
        """Return a rendered Digg-style pagination (by default).

        The callable *settings.PAGE_LIST_CALLABLE* can be used to customize
        how the pages are displayed. The callable takes the current page number
        and the total number of pages, and must return a sequence of page
        numbers that will be displayed. The sequence can contain other values:

            - *'previous'*: will display the previous page in that position;
            - *'next'*: will display the next page in that position;
            - *None*: a separator will be displayed in that position.

        Here is an example of custom calable that displays the previous page,
        then the first page, then a separator, then the current page, and
        finally the then next page::

            def get_page_numbers(current_page, num_pages):
                return ('previous', 1, None, current_page, 'next')

        If *settings.PAGE_LIST_CALLABLE* is None an internal callable is used,
        generating a Digg-style pagination. The value of
        *settings.PAGE_LIST_CALLABLE* can also be a dotted path to a callable.
        """
        if len(self) > 1:
            callable_or_path = settings.PAGE_LIST_CALLABLE
            if callable_or_path:
                if callable(callable_or_path):
                    pages_callable = callable_or_path
                else:
                    pages_callable = loaders.load_object(callable_or_path)
            else:
                pages_callable = utils.get_page_numbers
            pages = []
            for i in pages_callable(self._page.number, len(self)):
                if i is None:
                    pages.append(i)
                elif i == 'previous':
                    pages.append(self.previous())
                elif i == 'next':
                    pages.append(self.next())
                else:
                    pages.append(self[i])
            context = {'pages': pages}
            return loader.render_to_string('endless/show_pages.html', context)
        return ''

    def current(self):
        """Return the current page."""
        return self[self._page.number]

    def first(self):
        """Return the first page."""
        return self[1]

    def last(self):
        """Return the last page."""
        return self[len(self)]

    def previous(self):
        """Return the previous page.

        Return an empty string if current page is the first.
        """
        if self._page.has_previous():
            return self._endless_page(
                self._page.previous_page_number(),
                label=settings.PREVIOUS_LABEL)
        return ''

    def next(self):
        """Return the next page.

        Return an empty string if current page is the last.
        """
        if self._page.has_next():
            return self._endless_page(
                self._page.next_page_number(),
                label=settings.NEXT_LABEL)
        return ''
