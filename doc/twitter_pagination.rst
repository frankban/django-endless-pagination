Twitter-style Pagination
========================

As creative example, the developer wants Twitter-style pagination of 
entries of a blog post.

In *views.py* we have::

    def entry_index(request, template="myapp/entry_index.html"):
        context = {
            'objects': Entry.objects.all(),
        }
        return render_to_response(template, context, 
            context_instance=RequestContext(request))

In *myapp/entry_index.html*:

.. code-block:: html+django

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
the page template name in the context.

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
            
*myapp/entry_index.html* becomes:

.. code-block:: html+django

    <h2>Entries:</h2>
    {% include page_template %}
    
*myapp/entry_index_page.html* becomes:

.. code-block:: html+django

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

Splitting templates and putting the AJAX template name in the context 
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

Paginating objects
~~~~~~~~~~~~~~~~~~

Nothing remains but to change the page template, loading endless templatetags,
the jQuery library and the javascript file *endless.js* included 
in the distribution under ``/static/endless_pagination/js/``.

*myapp/entry_index.html* becomes:

.. code-block:: html+django

    {% block js %}
        {{ block.super }}
        <script src="/path/to/jquery.js" type="text/javascript" charset="utf-8"></script>
        <script src="/path/to/endless.js" type="text/javascript" charset="utf-8"></script>
    {% endblock %}
    
    <h2>Entries:</h2>
    {% include page_template %}

*myapp/entry_index_page.html* becomes:

.. code-block:: html+django

    {% load endless %}
    
    {% paginate objects %}
    {% for object in objects %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_more %}
    
Pagination on scroll
~~~~~~~~~~~~~~~~~~~~

If you want new items to load when the user scroll down the browser page
you can use the **pagination on scroll** feature: just load 
the *endless_on_scroll.js* javascript after the *endless.js* one in your template:

.. code-block:: html+django

    <script src="/path/to/jquery.js" type="text/javascript" charset="utf-8"></script>
    <script src="/path/to/endless.js" type="text/javascript" charset="utf-8"></script>
    <script src="/path/to/endless_on_scroll.js" type="text/javascript" charset="utf-8"></script>

That's all. See :doc:`templatetags_reference` to improve the use of 
included templatetags.

It is possible to set the bottom margin used for pagination on scroll 
(default is 1 pixel).

For example, if you want the pagination on scroll to be activated when
20 pixels remain to the end of the page:

.. code-block:: html+django

    <script src="/path/to/jquery.js" type="text/javascript" charset="utf-8"></script>
    <script src="/path/to/endless.js" type="text/javascript" charset="utf-8"></script>
    <script src="/path/to/endless_on_scroll.js" type="text/javascript" charset="utf-8"></script>
    
    {# add the lines below #}
    <script type="text/javascript" charset="utf-8">
        var endless_on_scroll_margin = 20;
    </script>
