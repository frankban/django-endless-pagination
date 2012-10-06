"""Django pagination tools supporting ajax, multiple and lazy pagination,
Twitter-style and Digg-style pagination.
"""

VERSION = (1, 2)


def get_version():
    """Return the Django Endless Pagination version as a string."""
    return '.'.join(map(str, VERSION))
