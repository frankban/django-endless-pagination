from django.views.generic import ListView
from django.core.exceptions import ImproperlyConfigured

from endless_pagination.settings import PAGE_LABEL

class AjaxListView(ListView):
    """
    A subclass of *django.views.generic.ListView* that allows AJAX
    pagination of a list of objects.
    """
    key = PAGE_LABEL
    page_template = None
    page_template_suffix = '_page'
    
    def get_page_template(self, **kwargs):
        """
        Only called if *page_template* is not given as a kwarg of 
        *self.as_view*.
        """
        opts = self.object_list.model._meta
        return "%s/%s%s%s.html" % (opts.app_label, opts.object_name.lower(), 
            self.template_name_suffix, self.page_template_suffix)
    
    def get_context_data(self, **kwargs):
        """
        Adds the *page_template* variable in the context.
        
        If the *page_template* is not given as a kwarg of the *as_view*
        method then it is invented using app label, model name
        (obviously if the list is a queryset), *self.template_name_suffix*
        and *self.page_template_suffix*.
        
        For instance, if the list is a queryset of *blog.Entry*, 
        the template will be *blog/entry_list_page.html*.
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
        """
        Switch the templates for AJAX requests.
        """
        request = self.request
        querystring_key = request.REQUEST.get("querystring_key", PAGE_LABEL)
        if request.is_ajax() and querystring_key == self.key:
            return [self.page_template]
        return super(AjaxListView, self).get_template_names()
