from endless_pagination.settings import PAGE_LABEL
from endless_pagination import exceptions

def get_page_number_from_request(request, page_label=PAGE_LABEL):
    """
    Get page number from *GET* or *POST* data.
    If the page dows not exists in *request*, or is not a number
    then 1 is returned.
    """
    try:
        return int(request.REQUEST[PAGE_LABEL])
    except (KeyError, TypeError, ValueError):
        return 1
        
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

def get_querystring_for_page(request, page_number, prefix="?"):
    """
    Return a querystring pointing to *page_number*.
    The querystring is prefixed by *prefix* (e.g.: "?page=2").
    """
    querydict = request.GET.copy()
    querydict[PAGE_LABEL] = page_number
    # for page number 1 there is no need for querystring
    if page_number == 1:
        del querydict[PAGE_LABEL]
    if querydict:
        return "%s%s" % (prefix, querydict.urlencode())
    return ""
        
    