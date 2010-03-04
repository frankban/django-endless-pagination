from django.template import Context, loader

from endless_pagination import settings, utils

# preload page templates
PAGE_TEMPLATE = loader.get_template("endless/page_link.html")
CURRENT_TEMPLATE = loader.get_template("endless/current_link.html")

class EndlessPage(object):
    """
    A page link representation.
    Interesting attributes:
    
        - *self.number*: the page number
        - *self.label*: the label of the link (normally the page number as string)
        - *self.url*: the url of the page (strting with "?")
        - *self.path*: the path of the page
        - *self.is_current*: return True if page is the current page displayed
        - *self.is_first*: return True if page is the first page
        - *self.is_last*:  return True if page is the last page
    """
    def __init__(self, request, number, current_number, total_number, 
        querystring_key, label=None, default_number=1):
        self.number = number
        self.label = unicode(number) if label is None else label
        self.querystring_key = querystring_key
        
        self.is_current = number == current_number
        self.is_first = number == 1
        self.is_last = number == total_number
        
        self.url = utils.get_querystring_for_page(request, number, 
            self.querystring_key, default_number=default_number)
        self.path = "%s%s" % (request.path, self.url)

    def __unicode__(self):
        """
        Render the page as a link.
        """
        context_instance = Context({
            'page': self, 
            'add_nofollow': settings.ADD_NOFOLLOW,
            'querystring_key': self.querystring_key,
        })
        template = CURRENT_TEMPLATE if self.is_current else PAGE_TEMPLATE
        return template.render(context_instance)
                
        
class PageList(object):
    """
    A sequence of endless pages.
    """
    def __init__(self, request, page, querystring_key, default_number=None):
        self._request = request
        self._page = page
        self._default_number = 1 if default_number is None else int(default_number)
        self._querystring_key = querystring_key
        
    def _endless_page(self, number, label=None):
        """
        Factory function that returns a EndlessPage instance.
        It works just like a partial constructor.
        """
        return EndlessPage(self._request, number, self._page.number, len(self), 
            self._querystring_key, label=label, 
            default_number=self._default_number)
    
    def __getitem__(self, value):
        # type conversion is needed beacuse in templates django performs a 
        # dictionary lookup before the attribute lokups 
        # (when a dot is encountered)
        try:
            value = int(value)
        except (TypeError, ValueError):
            # a TypeError says to django to continue with an attribute lookup
            raise TypeError
        if 1 <= value <= len(self):
            return self._endless_page(value)
        raise IndexError("page list index out of range")
        
    def __len__(self):
        """
        The length of the sequence is the total number of pages.
        """
        return self._page.paginator.num_pages
    
    def __iter__(self):
        """
        Iterate over all the endless pages (from first to last).
        """
        for i in range(len(self)):
            yield self[i+1]
        
    def __unicode__(self):
        """
        Return digg-style pagination (by default).
        The callable *settings.PAGE_LIST_CALLABLE* can be used to customize
        the pages that are displayed.
        The callable takes the current page number and the total number of pages
        and must return a sequence of page numbers that will be displayed.
        The sequence can contain other values:
        
            - *"previous"*: will display the previous page in that position
            - *"next"*: will display the next page in that position
            - *None*: a separator will be displayed in that position
            
        Here is an example of custom calable that displays previous page, then
        first page, then a separator, then current page, then next page::
        
            def get_page_numbers(current_page, num_pages):
                return ("previous", 1, None, current_page, "next")
        
        If *settings.PAGE_LIST_CALLABLE* is None an internal callable is used,
        generating a digg-style pagination.
        """
        if len(self) > 1:
            pages_callable = settings.PAGE_LIST_CALLABLE or utils.get_page_numbers
            pages = []
            for i in pages_callable(self._page.number, len(self)):
                if i is None:
                    pages.append(i)
                elif i == "previous":
                    pages.append(self.previous())
                elif i == "next":
                    pages.append(self.next())
                else:
                    pages.append(self[i])
            context = {'pages': pages}
            return loader.render_to_string("endless/show_pages.html", context)
        return u""
        
    def current(self):
        """
        Return current page.
        """
        return self[self._page.number]
        
    def first(self):
        """
        Return first page.
        """
        return self[1]
        
    def last(self):
        """
        Return last page.
        """
        return self[len(self)]
        
    def previous(self):
        """
        Return previous page or an empty string if current page is the first.
        """
        if self._page.has_previous():
            return self._endless_page(self._page.previous_page_number(), 
                label=settings.PREVIOUS_LABEL)
        return u""
        
    def next(self):
        """
        Return next page or an empty string if current page is the last.
        """
        if self._page.has_next():
            return self._endless_page(self._page.next_page_number(), 
                label=settings.NEXT_LABEL)
        return u""
