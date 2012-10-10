"""Test project URL patterns."""

from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView

from endless_pagination.decorators import (
    page_template,
    page_templates,
)

from project.views import base


urlpatterns = patterns('',
    url(r'^$',
        TemplateView.as_view(template_name="home.html"),
        name='home'),
    url(r'^digg/$',
        page_template('digg_page.html')(base),
        {'template': 'digg.html'},
        name='digg'),
    url(r'^twitter/$',
        page_template('twitter_page.html')(base),
        {'template': 'twitter.html'},
        name='twitter'),
    url(r'^onscroll/$',
        page_template('twitter_page.html')(base),
        {'template': 'onscroll.html'},
        name='onscroll'),
    url(r'^multiple/$',
        page_templates({
            'multiple_objects_page.html': 'objects-page',
            'multiple_items_page.html': 'items-page',
            'multiple_entries_page.html': 'entries-page',
        })(base),
        {'template': 'multiple.html', 'number': 21},
        name='multiple'),
)
