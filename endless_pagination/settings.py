from django.conf import settings

# How many objects are normally displayed in a page 
# (overwriteable by templatetag)
PER_PAGE = getattr(settings, "ENDLESS_PAGINATION_PER_PAGE", 10)
# The querystring key of the page number.
PAGE_LABEL = getattr(settings, "ENDLESS_PAGINATION_PAGE_LABEL", "page")
# See django *Paginator* definition of orphans.
ORPHANS = getattr(settings, "ENDLESS_PAGINATION_ORPHANS", 0)

# If you use the default *show_more* template, here you can customize
# the content of the loader hidden element
# Html is safe here, e.g. you can show your pretty animated gif:
#    ENDLESS_PAGINATION_LOADING = """
#        <img src="/static/img/loader.gif" alt="loading" />
#    """
LOADING = getattr(settings, 
    "ENDLESS_PAGINATION_LOADING", "loading")

# Labels for previous and next page links.
PREVIOUS_LABEL = getattr(settings, "ENDLESS_PAGINATION_PREVIOUS_LABEL", u"&lt;&lt;")
NEXT_LABEL = getattr(settings, "ENDLESS_PAGINATION_NEXT_LABEL", u"&gt;&gt;")

# Set to True if your seo alchemist wants all the links in digg-style
# pagination to be nofollow.
ADD_NOFOLLOW = getattr(settings, "ENDLESS_PAGINATION_ADD_NOFOLLOW", False)

# Callable that returns pages to be displayed.
# If None a default callable is used (that produces digg-style pagination).
PAGE_LIST_CALLABLE = getattr(settings, "ENDLESS_PAGINATION_PAGE_LIST_CALLABLE", None)

# Default callable returns pages for digg-style pagination, and depends
# on the settings below.
DEFAULT_CALLABLE_EXTREMES = getattr(settings, 
    "ENDLESS_PAGINATION_DEFAULT_CALLABLE_EXTREMES", 3)
DEFAULT_CALLABLE_AROUNDS = getattr(settings, 
    "ENDLESS_PAGINATION_DEFAULT_CALLABLE_AROUNDS", 2)
    
# Template variable name for *page_template* decorator.
TEMPLATE_VARNAME = getattr(settings, "ENDLESS_PAGINATION_TEMPLATE_VARNAME", "template")
