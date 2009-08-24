from django.conf import settings

# How many objects are normally displayed in a page 
# (overwriteable by templatetag)
PER_PAGE = getattr(settings, "ENDLESS_PAGINATION_PER_PAGE", 10)
# The querystring key of the page number.
PAGE_LABEL = getattr(settings, "ENDLESS_PAGINATION_PAGE_LABEL", "page")
# See django *Paginator* definition of orphans.
ORPHANS = getattr(settings, "ENDLESS_PAGINATION_ORPHANS", 0)

# The template used by *show_more* templatetag.
# You can provide your customized template that must meet the following rules:
# - *more* link is showed only if variable "querystring" is not False
# - the container (most external html element) class is *endless_container*
# - the *more* link and the loader hidden element live inside the container
# - the *more* link class is *endless_more*
# - the loader hidden element class is *endless_loading*
SHOW_MORE_TEMPLATE = getattr(settings, 
    "ENDLESS_PAGINATION_SHOW_MORE_TEMPLATE", "endless/show_more.html")
    
# If you use the default *show_more* template, here you can customize
# the content of the loader hidden element
# Html is safe here, e.g. you can show your pretty animated gif:
#    ENDLESS_PAGINATION_LOADING = """
#        <img src="/site_media/img/loader.gif" alt="loading" />
#    """
LOADING = getattr(settings, 
    "ENDLESS_PAGINATION_LOADING", "loading")
