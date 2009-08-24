==================
Endless Pagination
==================

:Author: Francesco Banconi <francesco.banconi@gmail.com>

.. contents:: Index

.. sectnum::

Introduction
============

This app may be used to provide Twitter-style ajaxed pagination. Future
developments will add support for normal Digg-style pagination.

The initial idea, which has guided the development of this application, 
is to allow ajax pagination of web contents in very few steps, as done by 
the excellent tool *django-pagination* 
(see http://github.com/ericflo/django-pagination/tree/master).


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

See *Customization* section of this documentation for other settings options.

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
        extra_context={}):
        context = {
            'objects': Entry.objects.all(),
        }
        context.upgrade(extra_context)
        return render_to_response(template, context, 
            context_instance=RequestContext(request))

Splitting templates and putting the ajax template name in the context 
is easily achievable at this point (using a builtin decorator).

*views.py* becomes::

    from endless_pagination.decorators import page_template
    
    @page_template("myapp/entry_index_page.html") # just add this decorator
    def entry_index(request, template="myapp/entry_index.html", 
        extra_context={}):
        context = {
            'objects': Entry.objects.all(),
        }
        context.upgrade(extra_context)
        return render_to_response(template, context, 
            context_instance=RequestContext(request))

This way, *endless-pagination* can be included in **generic views** too.

Pagination
~~~~~~~~~~

Nothing remains but to change the page template, loading endless templatetags and
the javascript file *endless.js* included in the distribution under ``/media/js/``.

*myapp/entry_index.html* becomes::

    {% block js %}
        {{ block.super }}
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

That's all. Read the next section of the documentation to improve the use of 
included templatetags.


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
    
You must use this tag before calling the ``{% show_more %}`` one.

show_more
~~~~~~~~~

Show the link to get the next page in a Twitter-like pagination.
Usage::

    {% show_more %}
    
Must be called after ``{% paginate objects %}``.


Customization
=============

You can customize the application using ``settings.py``.

- *ENDLESS_PAGINATION_PER_PAGE* (default=10): 
  How many objects are normally displayed in a page (overwriteable by templatetag).

- *ENDLESS_PAGINATION_PAGE_LABEL* (default="page"):
  The querystring key of the page number (e.g. ``http://example.com?page=2``)

- *ENDLESS_PAGINATION_ORPHANS* (default=0):
  See django *Paginator* definition of orphans.

- *ENDLESS_PAGINATION_SHOW_MORE_TEMPLATE* (default="endless/show_more.html"):
  The template used by *show_more* templatetag.
  You can provide your customized template that must meet the following rules:
  - *more* link is showed only if variable "querystring" is not False
  - the container (most external html element) class is *endless_container*
  - the *more* link and the loader hidden element live inside the container
  - the *more* link class is *endless_more*
  - the loader hidden element class is *endless_loading*
  
- *ENDLESS_PAGINATION_LOADING* (default="loading"):
  If you use the default *show_more* template, here you can customize
  the content of the loader hidden element
  Html is safe here, e.g. you can show your pretty animated gif::
  
     ENDLESS_PAGINATION_LOADING = """
         <img src="/site_media/img/loader.gif" alt="loading" />
     """

