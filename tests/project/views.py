"""Test project views."""

from django.shortcuts import render


LOREM = """Lorem ipsum dolor sit amet, consectetur adipisicing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
    nisi ut aliquip ex ea commodo consequat.
"""


def _make_items(title, number):
    """Make a *number* of items."""
    return [
        {'title': '{0} {1}'.format(title, i + 1), 'contents': LOREM}
        for i in range(number)
    ]


def base(request, extra_context=None, template=None):
    context = {
        'objects': _make_items('Object', 100),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)
