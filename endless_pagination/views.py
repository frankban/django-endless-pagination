"""Django Endless Pagination class based views."""

from django.core.exceptions import ImproperlyConfigured
from django.views.generic import ListView

from endless_pagination.settings import PAGE_LABEL


class AjaxListView(ListView):
    """Allows Ajax pagination of a list of objects.

    You can use this class based view in place of *ListView* in order to
    recreate the behaviour of the *page_template* decorator.

    For instance, assume you have this code (taken from Django docs)::

        from django.conf.urls.defaults import *
        from django.views.generic import ListView

        from books.models import Publisher

        urlpatterns = patterns('',
            (r'^publishers/$', ListView.as_view(model=Publisher)),
        )

    You want to Ajax paginate publishers, so, as seen, you need to switch
    the template if the request is Ajax and put the page template
    into the context as a variable named *page_template*.

    This is straightforward, you only need to replace the view class, e.g.::

        from django.conf.urls.defaults import *

        from books.models import Publisher

        from endless_pagination.views import AjaxListView

        urlpatterns = patterns('',
            (r'^publishers/$', AjaxListView.as_view(model=Publisher)),
        )

    NOTE: Django >= 1.3 is required to use this view.
    """
    key = PAGE_LABEL
    page_template = None
    page_template_suffix = '_page'

    def get_page_template(self, **kwargs):
        """Return the template name used for this request.

        Only called if *page_template* is not given as a kwarg of
        *self.as_view*.
        """
        opts = self.object_list.model._meta
        return '{0}/{1}{2}{3}.html'.format(
            opts.app_label,
            opts.object_name.lower(),
            self.template_name_suffix,
            self.page_template_suffix,
        )

    def get_context_data(self, **kwargs):
        """Adds the *page_template* variable in the context.

        If the *page_template* is not given as a kwarg of the *as_view*
        method then it is generated using app label, model name
        (obviously if the list is a queryset), *self.template_name_suffix*
        and *self.page_template_suffix*.

        For instance, if the list is a queryset of *blog.Entry*,
        the template will be ``blog/entry_list_page.html``.
        """
        context = super(AjaxListView, self).get_context_data(**kwargs)
        if self.page_template is None:
            if hasattr(self.object_list, 'model'):
                self.page_template = self.get_page_template(**kwargs)
            else:
                raise ImproperlyConfigured(
                    'AjaxListView requires a page_template')
        context['page_template'] = self.page_template
        return context

    def get_template_names(self):
        """Switch the templates for AJAX requests."""
        request = self.request
        querystring_key = request.REQUEST.get('querystring_key', PAGE_LABEL)
        if request.is_ajax() and querystring_key == self.key:
            return [self.page_template]
        return super(AjaxListView, self).get_template_names()
