"""Django Endless Pagination utility functions."""

from endless_pagination import exceptions
from endless_pagination.settings import (
    DEFAULT_CALLABLE_AROUNDS,
    DEFAULT_CALLABLE_EXTREMES,
    PAGE_LABEL,
)


def get_data_from_context(context):
    """Get the django paginator data object from the given *context*.

    The context is a dict-like object. If the context key ``endless``
    is not found, a *PaginationError* is raised.
    """
    try:
        return context['endless']
    except KeyError:
        raise exceptions.PaginationError(
            'Cannot find endless data in context.')


def get_page_number_from_request(
        request, querystring_key=PAGE_LABEL, default=1):
    """Retrieve the current page number from *GET* or *POST* data.

    If the page does not exists in *request*, or is not a number,
    then *default* number is returned.
    """
    try:
        return int(request.REQUEST[querystring_key])
    except (KeyError, TypeError, ValueError):
        return default


def get_page_numbers(
        current_page, num_pages, extremes=DEFAULT_CALLABLE_EXTREMES,
        arounds=DEFAULT_CALLABLE_AROUNDS):
    """Default callable for page listing.

    Produce a digg-style pagination.
    """
    page_range = range(1, num_pages + 1)
    pages = [] if current_page == 1 else ['previous']

    # Get first and last pages (extremes).
    first = page_range[:extremes]
    pages.extend(first)
    last = page_range[-extremes:]

    # Get the current pages (arounds).
    current_start = current_page - 1 - arounds
    if current_start < 0:
        current_start = 0
    current_end = current_page + arounds
    if current_end > num_pages:
        current_end = num_pages
    current = page_range[current_start:current_end]

    # Mix first with current pages.
    to_add = current
    if extremes:
        diff = current[0] - first[-1]
        if diff > 1:
            pages.append(None)
        elif diff < 1:
            to_add = current[abs(diff) + 1:]
    pages.extend(to_add)

    # Mix current with last pages.
    if extremes:
        diff = last[0] - current[-1]
        to_add = last
        if diff > 1:
            pages.append(None)
        elif diff < 1:
            to_add = last[abs(diff) + 1:]
        pages.extend(to_add)

    if current_page != num_pages:
        pages.append('next')
    return pages


def get_querystring_for_page(
        request, page_number, querystring_key, default_number=1):
    """Return a querystring pointing to *page_number*."""
    querydict = request.GET.copy()
    querydict[querystring_key] = page_number
    # For the default page number (usually 1) the querystring is not required.
    if page_number == default_number:
        del querydict[querystring_key]
    if 'querystring_key' in querydict:
        del querydict['querystring_key']
    if querydict:
        return '?' + querydict.urlencode()
    return ''
