Twitter-style Pagination
========================

Assuming the developer wants Twitter-style pagination of
entries of a blog post, in *views.py* we have::

    def entry_index(request, template='myapp/entry_index.html'):
        context = {
            'entries': Entry.objects.all(),
        }
        return render_to_response(
            template, context, context_instance=RequestContext(request))

In *myapp/entry_index.html*:

.. code-block:: html+django

    <h2>Entries:</h2>
    {% for entry in entries %}
        {# your code to show the entry #}
    {% endfor %}

Split the template
~~~~~~~~~~~~~~~~~~

The response to an Ajax request should not return the entire template,
but only the portion of the page to be updated or added.
So it is convenient to extract from the template the part containing the
entries, and use it to render the context if the request is Ajax.
The main template will include the extracted part, so it is convenient
to put the page template name in the context.

*views.py* becomes::

    def entry_index(
            request,
            template='myapp/entry_index.html',
            page_template='myapp/entry_index_page.html'):
        context = {
            'entries': Entry.objects.all(),
            'page_template': page_template,
        }
        if request.is_ajax():
            template = page_template
        return render_to_response(
            template, context, context_instance=RequestContext(request))

See below how to obtain the same result **just decorating the view**
(in a way compatible with generic views too).

*myapp/entry_index.html* becomes:

.. code-block:: html+django

    <h2>Entries:</h2>
    {% include page_template %}

*myapp/entry_index_page.html* becomes:

.. code-block:: html+django

    {% for entry in entries %}
        {# your code to show the entry #}
    {% endfor %}

A shortcut for ajaxed views
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A good practice in writing views is to allow other developers to inject
the template name and extra data, so that they are added to the context.
This allows the view to be easily reused. Let's resume the original view
with extra context injection:

*views.py*::

    def entry_index(
            request, template='myapp/entry_index.html', extra_context=None):
        context = {
            'entries': Entry.objects.all(),
        }
        if extra_context is not None:
            context.update(extra_context)
        return render_to_response(
            template, context, context_instance=RequestContext(request))

Splitting templates and putting the Ajax template name in the context
is easily achievable by using an included decorator.

*views.py* becomes::

    from endless_pagination.decorators import page_template

    @page_template('myapp/entry_index_page.html')  # just add this decorator
    def entry_index(
            request, template='myapp/entry_index.html', extra_context=None):
        context = {
            'entries': Entry.objects.all(),
        }
        if extra_context is not None:
            context.update(extra_context)
        return render_to_response(
            template, context, context_instance=RequestContext(request))

This way, *endless-pagination* can be included in **generic views** too.

See :doc:`generic_views` if you use Django >= 1.3 and you want to replicate
the same behavior using a class-based generic view.

Paginating objects
~~~~~~~~~~~~~~~~~~

All that's left is changing the page template and loading the endless
templatetags, the jQuery library and the jQuery plugin
``endless-pagination.js`` included in the distribution under
``/static/endless_pagination/js/``.

*myapp/entry_index.html* becomes:

.. code-block:: html+django

    <h2>Entries:</h2>
    {% include page_template %}

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>$.endlessPaginate();</script>
    {% endblock %}

*myapp/entry_index_page.html* becomes:

.. code-block:: html+django

    {% load endless %}

    {% paginate entries %}
    {% for entry in entries %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_more %}

See the :doc:`javascript` for a detailed explanation of how to integrate
JavaScript and Ajax features in Django Endless Pagination.

Pagination on scroll
~~~~~~~~~~~~~~~~~~~~

If you want new items to load when the user scroll down the browser page,
you can use the **pagination on scroll** feature: just set the
*paginateOnScroll* option of *$.endlessPaginate()* to *true*, e.g.:

.. code-block:: html+django

    <h2>Entries:</h2>
    {% include page_template %}

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>$.endlessPaginate({paginateOnScroll: true});</script>
    {% endblock %}

That's all. See the :doc:`templatetags_reference` to improve the use of
included templatetags.

It is possible to set the bottom margin used for pagination on scroll
(default is 1 pixel). For example, if you want the pagination on scroll
to be activated when 20 pixels remain to the end of the page:

.. code-block:: html+django

    <h2>Entries:</h2>
    {% include page_template %}

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>
            $.endlessPaginate({
                paginateOnScroll: true,
                paginateOnScrollMargin: 20
            });
        </script>
    {% endblock %}

Again, see the :doc:`javascript` page.

Before version 1.2
~~~~~~~~~~~~~~~~~~

Django Endless Pagination 1.2 introduces a redesigned Ajax support for
pagination. As seen above, Ajax can now be enabled using a brand new jQuery
plugin that can be found in
``static/endless_pagination/js/endless-pagination.js``.

For backward compatibility, the application still includes the two JavaScript
files ``endless.js`` and ``endless_on_scroll.js`` that were used before, so
that it is still possible to use code like this:

.. code-block:: html+django

    <script src="http://code.jquery.com/jquery-latest.js"></script>
    {# Deprecated. #}
    <script src="{{ STATIC_URL }}endless_pagination/js/endless.js"></script>

To enable pagination on scroll, the code was the following:

.. code-block:: html+django

    <script src="http://code.jquery.com/jquery-latest.js"></script>
    {# Deprecated. #}
    <script src="{{ STATIC_URL }}endless_pagination/js/endless.js"></script>
    <script src="{{ STATIC_URL }}endless_pagination/js/endless_on_scroll.js"></script>

However, please consider migrating as soon as possible: the old JavaScript
files are deprecated, are no longer maintained, and don't provide the new
JavaScript features.

Please refer to the :doc:`javascript` page for a detailed overview of the new
features and for instructions on **how to migrate** from the old JavaScript
files to the new one.
