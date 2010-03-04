import re

from django import template
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404

from endless_pagination import settings, models, utils

register = template.Library()

@register.tag
def paginate(parser, token):
    """
    Usage::
    
        {% paginate objects %}
    
    After this call, in the template context the *objects* variable is replaced
    with only the objects of the current page.
    
    You can also mantain your *objects* original variable (commonly a queryset)
    and add to context another name referring to objects of the current page, 
    e.g.::
    
        {% paginate objects as page_objects %}
        
    The number of paginated object is taken from settings, but you can
    override the default, e.g.::
    
        {% paginate 20 objects %}
        
    Of course you can mix it all::
    
        {% paginate 20 objects as paginated_objects %}
        
    By default, the first page is displayed the first time you load the page,
    but you can easily change this, e.g.::
    
        {% paginate objects starting from page 3 %}
        
    This can be also achieved using a template variable you passed in the
    context, e.g.::
    
        {% paginate objects starting from page page_number %}
        
    If the passed page number does not exist then first page is displayed.
    
    If you have multiple paginations in the same page, you can change the
    querydict key for the single pagination, e.g.::
    
        {% paginate objects using article_page %}
    
    Again, you can mix it all (the order of arguments is important)::
    
        {% paginate 20 objects starting from page 3 using page_key as paginated_objects %}
    
    You must use this tag before calling the {% show_more %} one.
    """
    # args validation
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        message = "%r tag requires arguments" % token.contents.split()[0]
        raise template.TemplateSyntaxError, message
        
    # use regexp to catch args    
    p = r'^((?P<per_page>\d+)\s+)?(?P<objects>\w+)(\s+starting\s+from\s+page\s+(?P<number>\w+))?(\s+using\s+(?P<key>\w+))?(\s+as\s+(?P<var_name>\w+))?$'
    e = re.compile(p)
    
    match = e.match(args)
    if match is None:
        message = "Invalid arguments for %r tag" % token.contents.split()[0]
        raise template.TemplateSyntaxError, message
    
    # get objects
    kwargs = match.groupdict()
    objects = kwargs.pop("objects")
    
    # call the node
    return PaginateNode(objects, **kwargs)
    
class PaginateNode(template.Node):
    """
    Insert into context the objects of the current page and
    the django paginator's *page* object.
    """
    def __init__(self, objects, per_page=None, var_name=None, number=None, key=None):
        self.objects = template.Variable(objects)
        # if var_name is not passed then will be queryset name
        self.var_name = objects if var_name is None else var_name
        # if per_page is not passed then is taken from settings
        self.per_page = settings.PER_PAGE if per_page is None else int(per_page)
        # manage page number when is not specified in querystring
        self.page_number_variable = None
        if number is None:
            self.page_number = 1
        elif number.isdigit():
            self.page_number = int(number)
        else:
            self.page_number_variable = template.Variable(number)
        # set the querystring key attribute
        self.querystring_key = key
    
    def render(self, context):
        # get page number to use if it is not specified in querystring
        if self.page_number_variable is None:
            default_number = self.page_number
        else:
            default_number = int(self.page_number_variable.resolve(context))
        
        # user can override settings querystring key in the template
        querystring_key = self.querystring_key or settings.PAGE_LABEL
            
        # request is used to get requested page number
        page_number = utils.get_page_number_from_request(context["request"],
            querystring_key, default=default_number)
        
        objects = self.objects.resolve(context)
        paginator = Paginator(objects, self.per_page, orphans=settings.ORPHANS)
        
        # get the page, user in settings can manage the case it is empty
        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = paginator.page(1)
        
        # populate context with new data
        context["endless_default_number"] = default_number
        context["endless_querystring_key"] = querystring_key
        context["endless_page"] = page
        context[self.var_name] = page.object_list
        return ""

    
@register.inclusion_tag("endless/show_more.html", takes_context=True)
def show_more(context):
    """
    Show the link to get the next page in a Twitter-like pagination.
    Usage::
    
        {% show_more %}
        
    Must be called after {% paginate objects %}.
    """
    # this can raise a PaginationError 
    # (you have to call paginate before including the show more template)
    page = utils.get_page_from_context(context)
    # show the template only if there is a next page
    if page.has_next():
        request = context["request"]
        page_number = page.next_page_number()
        # querystring
        querystring_key = context["endless_querystring_key"]
        querystring = utils.get_querystring_for_page(request, page_number,
            querystring_key, default_number=context["endless_default_number"])
        return {
            'path': request.path,
            'querystring_key': querystring_key,
            'querystring': querystring,
            'loading': settings.LOADING,
        }
    # no next page, nothing to see
    return {}
    
    
@register.tag
def get_pages(parser, token):
    """
    Usage::
    
        {% get_pages %}
    
    This is mostly used for digg-style pagination.
    This call inserts in the template context a *pages* variable, as a sequence
    of page links. You can use *pages* in different ways:
    
        - just print *pages* and you will get digg-style pagination displayed::
    
            {{ pages }}
            
        - display pages count::
        
            {{ pages|length }}
            
        - get a specific page::
            
            {# the current selected page #}
            {{ pages.current }} 
            
            {# the first page #}
            {{ pages.first }} 
            
            {# the last page #}
            {{ pages.last }} 
            
            {# the previous page (or nothing if you are on first page) #}
            {{ pages.previous }} 
            
            {# the next page (or nothing if you are in last page) #}
            {{ pages.next }}
            
            {# the third page #}
            {{ pages.3 }}
            {# this means page.1 is the same as page.first #}
            
        - iterate over *pages* to get all pages::
        
            {% for page in pages %}
                {# display page link #}
                {{ page }} 
                
                {# the page url (beginning with "?") #}
                {{ page.url }} 
                
                {# the page path #}
                {{ page.path }} 
                
                {# the page number #}
                {{ page.number }} 
                
                {# a string representing the page (commonly the page number) #}
                {{ page.label }}
                
                {# check if the page is the current one #}
                {{ page.is_current }}
                
                {# check if the page is the first one #}
                {{ page.is_first }}
                
                {# check if the page is the last one #}
                {{ page.is_last }} 
            {% endfor %}
        
    You can change the variable name, e.g.::
    
        {% get_pages as page_links %}
    
    Must be called after {% paginate objects %}.
    """
    # args validation
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        var_name = "pages"
    else:
        args = args.split()
        if len(args) == 2 and args[0] == "as":
            var_name = args[1]
        else:
            message = "%r tag invalid arguments" % tag_name
            raise template.TemplateSyntaxError, message
            
    # call the node
    return GetPagesNode(var_name)
    
class GetPagesNode(template.Node):
    """
    Insert into context the page list.
    """
    def __init__(self, var_name):
        self.var_name = var_name 
    
    def render(self, context):
        # this can raise a PaginationError 
        # (you have to call paginate before including the get pages template)
        page = utils.get_page_from_context(context)
        default_number = context.get("endless_default_number")
        
        # put the PageList instance in the context
        context[self.var_name] = models.PageList(context["request"], page,
            context["endless_querystring_key"],
            default_number=context["endless_default_number"])
        return ""
        
        
@register.tag
def show_pages(parser, token):
    """
    Show page links.
    Usage::
    
        {% show_pages %}
        
    It is only a shortcut for::
    
        {% get_pages %}
        {{ pages }}
    
    You can set *ENDLESS_PAGE_LIST_CALLABLE* in your settings.py as a callable 
    used to customize the pages that are displayed.
    The callable takes the current page number and the total number of pages
    and must return a sequence of page numbers that will be displayed.
    The sequence can contain other values:
    
        - *"previous"*: will display the previous page in that position
        - *"next"*: will display the next page in that position
        - *None*: a separator will be displayed in that position
        
    Here is an example of custom calable that displays previous page, then
    first page, then a separator, then current page, then next page::
    
        def get_page_numbers(current_page, num_pages):
            return ("previous", 1, "...", current_page, "next")
    
    If *ENDLESS_PAGE_LIST_CALLABLE* is *None* an internal callable is used,
    generating a digg-style pagination.
    
    Must be called after {% paginate objects %}.
    """
    # args validation
    if len(token.contents.split()) != 1:
        message = "%r tag takes no arguments" % token.contents.split()[0]
        raise template.TemplateSyntaxError, message
    # call the node
    return ShowPagesNode()
    
class ShowPagesNode(template.Node):
    """
    Show the pagination.
    """
    def render(self, context):
        # this can raise a PaginationError 
        # (you have to call paginate before including the get pages template)
        page = utils.get_page_from_context(context)
        # unicode representation of the sequence of pages
        pages = models.PageList(context["request"], page, 
            context["endless_querystring_key"],
            default_number=context["endless_default_number"])
        return unicode(pages)
        
        
@register.tag
def show_current_number(parser, token):
    """
    Just show current page number (useful in page titles).
    Usage::
    
        {% show_current_number %}
        
    If you use multiple paginations in the same page you can get the page
    number for a specific pagination using the querystring key, e.g.::
    
        {% show_current_number using mykey %}
        
    Default page when no querystring is specified is 1. If you changed in the 
    *paginate* template tag, you have to call  *show_current_number* 
    according to your choice, e.g.::
        
        {% show_current_number starting from page 3 %}
    
    This can be also achieved using a template variable you passed in the
    context, e.g.::
    
        {% show_current_number starting from page page_number %}
        
    Of course, you can mix it all (the order of arguments is important)::
    
        {% show_current_number starting from page 3 using mykey %}
    """
    # args validation
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        tag_name = token.contents[0]
        number = None
        key = None
    else:
        # use regexp to catch args    
        p = r'^(starting\s+from\s+page\s+(?P<number>\w+))?\s*(using\s+(?P<key>\w+))?$'
        e = re.compile(p)
        match = e.match(args)
        if match is None:
            message = "Invalid arguments for %r tag" % tag_name
            raise template.TemplateSyntaxError, message    
        # get objects
        groupdict = match.groupdict()
        number = groupdict["number"]
        key = groupdict["key"]
    # call the node
    return ShowCurrentNumberNode(number, key)
    
class ShowCurrentNumberNode(template.Node):
    """
    Show the page number taken from context.
    """
    def __init__(self, number, key):
        self.page_number_variable = None
        if number is None:
            self.page_number = 1
        elif number.isdigit():
            self.page_number = int(number)
        else:
            self.page_number_variable = template.Variable(number)

        self.querystring_key = key or settings.PAGE_LABEL
    
    def render(self, context):
        if self.page_number_variable is None:
            default_number = self.page_number
        else:
            default_number = int(self.page_number_variable.resolve(context))
        page_number = utils.get_page_number_from_request(context["request"],
            self.querystring_key, default=default_number)
        return unicode(page_number)
