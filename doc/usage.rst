==================
Endless Pagination
==================

:Author: Francesco Banconi <francesco.banconi@gmail.com>

.. contents:: Index

.. sectnum::


Introduction
============

This app can be used to provide Twitter-style or Digg-style pagination, with
optional ajax support and other features like multiple or lazy poagination.
The initial idea, which has guided the development of this application, 
is to allow pagination of web contents in very few steps.


Installation
============

The ``endless_pagination`` package, included in the distribution, should be
placed on the *Python path*.

Or just ``easy_install django-endless-pagination``.

Requirements
~~~~~~~~~~~~

- Python >= 2.5
- Django >= 1.0
- jQuery >= 1.3


Usage
=====

Settings
~~~~~~~~

Add the request context processor in your *settings.py*, e.g.::
    
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    TEMPLATE_CONTEXT_PROCESSORS += (
         'django.core.context_processors.request',
    )
    
Add ``'endless_pagination'`` to the ``INSTALLED_APPS`` in your *settings.py*.

See *Customization* section in this documentation for other settings options.

Let's start
~~~~~~~~~~~

As creative example, the developer wants pagination of entries of a blog post.

In *views.py* we have::

    def entry_index(request, template="myapp/entry_index.html"):
        context = {
            'objects': Entry.objects.all(),
        }
        return render_to_response(template, context, 
            context_instance=RequestContext(request))

In *myapp/entry_index.html*::

    <h2>Entries:</h2>
    {% for object in objects %}
        {# your code to show the entry #}
    {% endfor %}

Split the template
~~~~~~~~~~~~~~~~~~

A response to an AJAX request should not return the entire template, 
but only the portion of the page to update or add. 
So it is convenient to extrapolate from the template the part containing entries 
and use the new one to render the context if the request is AJAX.
The main template will include the other, so it is convenient to put
the page template in the context.

*views.py* becomes::
    
    def entry_index(request, 
        template="myapp/entry_index.html", 
        page_template="myapp/entry_index_page.html"):
        context = {
            'objects': Entry.objects.all(),
            'page_template': page_template,
        }
        if request.is_ajax(): 
            template = page_template
        return render_to_response(template, context, 
            context_instance=RequestContext(request))
            
See below how to obtain the same result **just decorating the view**
(in a way compatible with generic views too).
            
*myapp/entry_index.html* becomes::

    <h2>Entries:</h2>
    {% include page_template %}
    
*myapp/entry_index_page.html* becomes::

    {% for object in objects %}
        {# your code to show the entry #}
    {% endfor %}

A shortcut for ajaxed views
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A good practice in writing views is to allow other developers to inject
the template name and extra data to be added to the context.
This allows the view to be easily reused. Let's resume the original view
with extra context injection:

*views.py*::

    def entry_index(request, template="myapp/entry_index.html", 
        extra_context=None):
        context = {
            'objects': Entry.objects.all(),
        }
        if extra_context is not None:
            context.update(extra_context)
        return render_to_response(template, context, 
            context_instance=RequestContext(request))

Splitting templates and putting the ajax template name in the context 
is easily achievable at this point (using a builtin decorator).

*views.py* becomes::

    from endless_pagination.decorators import page_template
    
    @page_template("myapp/entry_index_page.html") # just add this decorator
    def entry_index(request, template="myapp/entry_index.html", 
        extra_context=None):
        context = {
            'objects': Entry.objects.all(),
        }
        if extra_context is not None:
            context.update(extra_context)
        return render_to_response(template, context, 
            context_instance=RequestContext(request))

This way, *endless-pagination* can be included in **generic views** too.

Pagination
~~~~~~~~~~

Nothing remains but to change the page template, loading endless templatetags,
the jQuery library and the javascript file *endless.js* included 
in the distribution under ``/media/js/``.

*myapp/entry_index.html* becomes::

    {% block js %}
        {{ block.super }}
        <script src="/path/to/jquery.js" type="text/javascript" charset="utf-8"></script>
        <script src="/path/to/endless.js" type="text/javascript" charset="utf-8"></script>
    {% endblock %}
    
    <h2>Entries:</h2>
    {% include page_template %}

*myapp/entry_index_page.html* becomes::

    {% load endless %}
    
    {% paginate objects %}
    {% for object in objects %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_more %}

If you want new items to load when the user scroll down the browser page
you can use the **pagination on scroll** feature: just load 
the *endless_on_scroll.js* javascript after the *endless.js* one in your template::

    <script src="/path/to/jquery.js" type="text/javascript" charset="utf-8"></script>
    <script src="/path/to/endless.js" type="text/javascript" charset="utf-8"></script>
    <script src="/path/to/endless_on_scroll.js" type="text/javascript" charset="utf-8"></script>

That's all. Read the next section of the documentation to improve the use of 
included templatetags.


Digg-style pagination
=====================

Digg-style pagination of queryset objects is really easy to implement.
If AJAX pagination is not needed, all you have to do is modify the template, e.g.::

    {% load endless %}
    
    {% paginate objects %}
    {% for object in objects %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_pages %}
    
That's it!
If you want to display only previous and next links (in a page-by-page pagination)
you need to use the lower level *get_pages* templatetag (see reference below),
e.g.::

    {% load endless %}
    
    {% paginate objects %}
    {% for object in objects %}
        {# your code to show the entry #}
    {% endfor %}
    {% get_pages %}
    {{ pages.previous }} {{ pages.next }}

See the paragraph *Customization* that explains how to customize arrows
of previous and next pages.

Adding ajax
~~~~~~~~~~~

The view is exactly the same as in *show_more* twitter-style pagination::

    from endless_pagination.decorators import page_template
    
    @page_template("myapp/entry_index_page.html") # just add this decorator
    def entry_index(request, template="myapp/entry_index.html", 
        extra_context=None):
        context = {
            'objects': Entry.objects.all(),
        }
        if extra_context is not None:
            context.update(extra_context)
        return render_to_response(template, context, 
            context_instance=RequestContext(request))
            
Of course you have to split templates, but this time a container for 
page template is needed too, and must have a class named *endless_page_template*.

*myapp/entry_index.html* becomes::

    {% block js %}
        {{ block.super }}
        <script src="/path/to/jquery.js" type="text/javascript" charset="utf-8"></script>
        <script src="/path/to/endless.js" type="text/javascript" charset="utf-8"></script>
    {% endblock %}
    
    <h2>Entries:</h2>
    <div class="endless_page_template">
        {% include page_template %}
    </div>

*myapp/entry_index_page.html* becomes::

    {% load endless %}
    
    {% paginate objects %}
    {% for object in objects %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_pages %}
    
Done.


Multiple pagination in the same page
====================================

Sometimes it is necessary to show different types of paginated objects in the 
same page. In this case we have to associate to every pagination a different 
querystring key. 
Normally, the key used is the one specified in *ENDLESS_PAGINATION_PAGE_LABEL*, 
but in the case of multiple pagination the application provides a simple way to 
override the settings. 
If you do not need ajax, the only file you need to edit
is the template. Here is a usecase example with 2 different paginations 
(*objects* and *other_objects*) in the same page, but there is no limit to the 
number of different paginations in a page::

    {% load endless %}
    
    {% paginate objects %}
    {% for object in objects %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_pages %}
    
    {% paginate other_objects using "other_objects_page" %} {# <-- a new querystring key #}
    {% for object in other_objects %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_pages %}
    
The *using* argument of the *paginate* template tag allows you to choose the 
name of the querystring key used to track the page number.
If not specified the system falls back to *settings.ENDLESS_PAGINATION_PAGE_LABEL*.
In the example above, the url *http://example.com?page=2&other_objects_page=3* 
requests the second page of *objects* and the third page of *other_objects*.

The name of the querystring key can also be dinamically passed in the template
context, e.g.::

    {% paginate other_objects using page_variable %} {# <-- page_variable is not surrounded by quotes #}
    
You can use any style of pagination: *show_pages*, *get_pages*, *show_more* etc...

Adding ajax for multiple pagination
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Obviously each pagination needs a template for the page content.
Remember to box each page in a div with a class called *endless_page_template*.

*myapp/entry_index.html*::

    {% block js %}
        {{ block.super }}
        <script src="/path/to/jquery.js" type="text/javascript" charset="utf-8"></script>
        <script src="/path/to/endless.js" type="text/javascript" charset="utf-8"></script>
    {% endblock %}

    <h2>Entries:</h2>
    <div class="endless_page_template">
        {% include "myapp/entries_page.html" %}
    </div>
    
    <h2>Other entries:</h2>
    <div class="endless_page_template">
        {% include "myapp/other_entries_page.html" %}
    </div>

*myapp/entries_page.html*::

    {% load endless %}

    {% paginate objects %}
    {% for object in objects %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_pages %}
    
*myapp/other_entries_page.html*::

    {% load endless %}

    {% paginate other_objects using other_objects_page %}
    {% for object in other_objects %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_pages %}

Again the decorator *page_template* simplifies the management of ajax requests 
in views. You must, however, map different paginations to different page templates.
You can chain decorator's calls relating a template with the associated 
querystring key, e.g.::

    from endless_pagination.decorators import page_template
    
    @page_template("myapp/entries_page.html")
    @page_template("myapp/other_entries_page.html", key="other_objects_page")
    def entry_index(request, template="myapp/entry_index.html", 
        extra_context=None):
        context = {
            'objects': Entry.objects.all(),
            'other_objects': OtherEntry.objects.all(),
        }
        if extra_context is not None:
            context.update(extra_context)
        return render_to_response(template, context, 
            context_instance=RequestContext(request))
            
As seen in previous examples, if you do not specify the *key* kwarg in the 
decorator, then the page template is associated to the querystring key
defined in the settings.

You can use the *page_templates* (note the trailing *s*) decorator in 
substitution of a decorator chain when you need multiple ajax pagination.
The previous example can be written::

    from endless_pagination.decorators import page_templates

    @page_templates({
        "myapp/entries_page.html": None, 
        "myapp/other_entries_page.html": "other_objects_page",
    })
    def entry_index() ...
    
    
Lazy pagination
===============

Usually pagination requires to hit the database to get the total number of items 
to display. Lazy pagination avoids this *select count* query and results in a 
faster page load, with a disadvantage: you can't know the total number of pages.
For this reason it is better to use lazy pagination in conjunction with 
twitter-style pagination (e.g. using the *show_more* template tag).

To switch to lazy pagination all you have to do is to use the 
*{% lazy_paginate %}* template tag instead of the *{% paginate %}* one, e.g.::
    
    {% load endless %}
    
    {% lazy_paginate objects %}
    {% for object in objects %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_more %}

The *lazy_paginate* tag can take all the args of *paginate* 
(see below the templatetags reference).


Templatetags reference
======================

paginate
~~~~~~~~

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

In this case *article_page* is intended to be a context variable, but you can
hardcode the key using quotes, e.g.::

    {% paginate objects using 'articles_at_page' %}

Again, you can mix it all (the order of arguments is important)::

    {% paginate 20 objects starting from page 3 using page_key as paginated_objects %}

Additionally you can pass a path to be used for the pagination::

    {% paginate 20 objects using page_key with pagination_url as paginated_objects %}
    
**New in version 0.7**
If you want the first page to contain a different number of items than
subsequent pages you can separate the two values with a comma, e.g. if 
you want 3 items on the first page and 10 on other pages::

    {% paginate 3,10 objects %}

You must use this tag before calling the {% show_more %} one.

lazy_paginate
~~~~~~~~~~~~~

Paginate objects without hitting the database with a *select count* query.

Use this the same way as *paginate* tag when you are not interested
in the total number of pages.

show_more
~~~~~~~~~

Show the link to get the next page in a Twitter-like pagination.
Usage::

    {% show_more %}
  
Alternatively you can override the label passed to the default template::

    {% show_more "even more" %}

**New in version 0.7**
You can override the loading text too::

    {% show_more "even more" "working" %}
    
Must be called after ``{% paginate objects %}``.

get_pages
~~~~~~~~~

Usage::

    {% get_pages %}

This is mostly used for digg-style pagination.
This call inserts in the template context a *pages* variable, as a sequence
of page links. You can use *pages* in different ways:

just print *pages* and you will get digg-style pagination displayed::

    {{ pages }}
    
display pages count::

    {{ pages|length }}
    
get a specific page::
    
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
    
iterate over *pages* to get all pages::

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

Must be called after ``{% paginate objects %}``.

show_pages
~~~~~~~~~~

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
    
Here is an example of custom callable that displays previous page, then
first page, then a separator, then current page, then next page::

    def get_page_numbers(current_page, num_pages):
        return ("previous", 1, None, current_page, "next")

If *ENDLESS_PAGE_LIST_CALLABLE* is *None* an internal callable is used,
generating a digg-style pagination.

Must be called after ``{% paginate objects %}``.

show_current_number
~~~~~~~~~~~~~~~~~~~

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


Customization
=============

You can customize the application using ``settings.py``.

- *ENDLESS_PAGINATION_PER_PAGE* (default=10): 
  How many objects are normally displayed in a page (overwriteable by templatetag).

- *ENDLESS_PAGINATION_PAGE_LABEL* (default="page"):
  The querystring key of the page number (e.g. ``http://example.com?page=2``)

- *ENDLESS_PAGINATION_ORPHANS* (default=0):
  See django *Paginator* definition of orphans.

- *ENDLESS_PAGINATION_LOADING* (default="loading"):
  If you use the default *show_more* template, here you can customize
  the content of the loader hidden element
  Html is safe here, e.g. you can show your pretty animated gif
  


::

     ENDLESS_PAGINATION_LOADING = """
         <img src="/site_media/img/loader.gif" alt="loading" />
     """
  
     
- *ENDLESS_PAGINATION_PREVIOUS_LABEL* (default=u"&lt;&lt;") and *NEXT_LABEL* (default=u"&gt;&gt;"):
  Labels for previous and next page links.
  
- *ENDLESS_PAGINATION_ADD_NOFOLLOW* (default=False):  # 
  Set to True if your seo alchemist wants search engines not to follow 
  pagination links.
  
- *ENDLESS_PAGINATION_PAGE_LIST_CALLABLE* (default=None):
  Callable that returns pages to be displayed.
  If None a default callable is used (that produces digg-style pagination).
  
  Default callable returns pages for digg-style pagination, and depends
  on the settings below:
  
- *ENDLESS_PAGINATION_DEFAULT_CALLABLE_EXTREMES* (default=3)
- *ENDLESS_PAGINATION_DEFAULT_CALLABLE_AROUNDS* (default=2)

- *ENDLESS_PAGINATION_TEMPLATE_VARNAME* (default="template"):
  Template variable name used by *page_template* decorator.
     
Template and css
~~~~~~~~~~~~~~~~

You can override the default template for *show_more* templatetag following
some rules:

- *more* link is showed only if variable ``querystring`` is not False
- the container (most external html element) class is *endless_container*
- the *more* link and the loader hidden element live inside the container
- the *more* link class is *endless_more*
- the *more* link rel attribute is *{{ querystring_key }}*
- the loader hidden element class is *endless_loading*

Application comes with English, Italian and German i18n.


Related projects
================

Try out http://code.google.com/p/django-yafinder/ if you need to add filter
and sort capabilities to your index pages.


Thanks
======

This application was initially inspired by the excellent tool *django-pagination* 
(see http://github.com/ericflo/django-pagination/tree/master).

Thanks to Jannis Leidel for his contributions in improving 
the application with some new features.
