"""Navigation bar context processor."""

import platform

import django
from django.core.urlresolvers import reverse

import endless_pagination


VOICES = (
    # Name and label pairs.
    ('digg', 'Digg-style'),
    ('twitter', 'Twitter-style'),
)


def navbar(request):
    """Generate a list of voices for the navigation bar."""
    voice_list = []
    current_path = request.path
    for name, label in VOICES:
        path = reverse(name)
        voice_list.append({
            'label': label,
            'path': path,
            'is_active': path == current_path,
        })
    return {'navbar': voice_list}


def versions(request):
    """Add to context the version numbers of relevant apps."""
    values = (
        ('Python', platform.python_version()),
        ('Django', django.get_version()),
        ('Endless Pagination', endless_pagination.get_version()),
    )
    return {'versions': values}
