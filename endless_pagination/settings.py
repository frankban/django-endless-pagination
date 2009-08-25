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
#        <img src="/site_media/img/loader.gif" alt="loading" />
#    """
LOADING = getattr(settings, 
    "ENDLESS_PAGINATION_LOADING", "loading")
