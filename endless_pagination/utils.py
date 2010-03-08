from endless_pagination.settings import DEFAULT_CALLABLE_EXTREMES, DEFAULT_CALLABLE_AROUNDS
from endless_pagination import exceptions

def get_page_number_from_request(request, querystring_key, default=1):
    """
    Get page number from *GET* or *POST* data.
    If the page does not exists in *request*, or is not a number
    then *default* number is returned.
    """
    try:
        return int(request.REQUEST[querystring_key])
    except (KeyError, TypeError, ValueError):
        return default
        
def get_page_from_context(context):
    """
    Get the django paginator page object from a *context* (a dict like object).
    If the context key "endless_page" is not found, a PaginationError
    is raised.
    """
    try:
        return context["endless_page"]
    except KeyError:
        raise exceptions.PaginationError("Cannot find endless page in context.")
        
def get_querystring_for_page(request, page_number, querystring_key,
    default_number=1, prefix="?"):
    """
    Return a querystring pointing to *page_number*.
    The querystring is prefixed by *prefix* (e.g.: "?page=2").
    """
    querydict = request.GET.copy()
    querydict[querystring_key] = page_number
    # for page number 1 there is no need for querystring
    if page_number == default_number:
        del querydict[querystring_key]
    if "querystring_key" in querydict:
        del querydict["querystring_key"]
    if querydict:
        return "%s%s" % (prefix, querydict.urlencode())
    return ""
    
def get_page_numbers(current_page, num_pages, 
    extremes=DEFAULT_CALLABLE_EXTREMES, arounds=DEFAULT_CALLABLE_AROUNDS):
    """
    Default callable for page listing.
    Produces a digg-style pagination.
    """
    page_range = range(1, num_pages+1)
    pages = ["previous"]
    
    # get first and last pages (extremes)
    first = page_range[:extremes]
    pages.extend(first)
    last = page_range[-extremes:]
    
    # get current pages (arounds)
    current_start = current_page - 1 - arounds
    if current_start < 0:
        current_start = 0
    current_end = current_page + arounds
    if current_end > num_pages:
        current_end = num_pages
    current = page_range[current_start:current_end]
    
    # mix first with current pages
    diff = current[0] - first[-1]
    to_add = current
    if diff > 1:
        pages.append(None)
    elif diff < 1:
        to_add = current[abs(diff)+1:]
    pages.extend(to_add)
    
    # mix current with last pages
    diff = last[0] - current[-1]
    to_add = last
    if diff > 1:
        pages.append(None)
    elif diff < 1:
        to_add = last[abs(diff)+1:]
    pages.extend(to_add)
    
    pages.append("next")
    return pages
