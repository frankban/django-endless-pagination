"""Test project URL patterns."""

from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView

from endless_pagination.decorators import (
    page_template,
    page_templates,
)

from project.views import generic


urlpatterns = patterns('',
    url(r'^$',
        TemplateView.as_view(template_name="home.html"),
        name='home'),
    url(r'^complete/$',
        page_templates({
            'complete/objects_page.html': 'objects-page',
            'complete/items_page.html': 'items-page',
            'complete/entries_page.html': 'entries-page',
            'complete/articles_page.html': 'articles-page',
        })(generic),
        {'template': 'complete/index.html', 'number': 21},
        name='complete'),
    url(r'^digg/$',
        page_template('digg/page.html')(generic),
        {'template': 'digg/index.html'},
        name='digg'),
    url(r'^twitter/$',
        page_template('twitter/page.html')(generic),
        {'template': 'twitter/index.html'},
        name='twitter'),
    url(r'^onscroll/$',
        page_template('onscroll/page.html')(generic),
        {'template': 'onscroll/index.html'},
        name='onscroll'),
    url(r'^multiple/$',
        page_templates({
            'multiple/objects_page.html': 'objects-page',
            'multiple/items_page.html': 'items-page',
            'multiple/entries_page.html': 'entries-page',
        })(generic),
        {'template': 'multiple/index.html', 'number': 21},
        name='multiple'),
)
