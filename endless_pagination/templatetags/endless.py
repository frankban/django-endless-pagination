import re

from django import template
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404

from endless_pagination import settings, utils

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
        
    You must use this tag before calling the {% show_more %} one.
    """
    # args validation
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        message = "%r tag requires arguments" % token.contents.split()[0]
        raise template.TemplateSyntaxError, message
        
    # use regexp to catch args    
    p = r'^\s*((?P<per_page>\d+)\s+)?(?P<objects>\w+)(\s+as\s+(?P<var_name>\w+))?\s*$'
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
    def __init__(self, objects, per_page=None, var_name=None):
        self.objects = template.Variable(objects)
        # if var_name is not passed then will be queryset name
        self.var_name = objects if var_name is None else var_name
        # if per_page is not passed then is taken from settings
        self.per_page = settings.PER_PAGE if per_page is None else int(per_page)
    
    def render(self, context):
        # request is used to get requested page number
        page_number = utils.get_page_number_from_request(context["request"])
        
        objects = self.objects.resolve(context)
        paginator = Paginator(objects, self.per_page, orphans=settings.ORPHANS)
        
        # get the page, user in settings can manage the case it is empty
        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = paginator.page(1)
        
        # populate context with new data
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
        querystring = utils.get_querystring_for_page(request, page_number)
        return {
            'path': request.path,
            'querystring': querystring,
            'loading': settings.LOADING,
        }
    # no next page, nothing to see
    return {}
