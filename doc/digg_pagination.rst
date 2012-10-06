Digg-style pagination
=====================

Digg-style pagination of queryset objects is really easy to implement. If Ajax
pagination is not needed, all you have to do is modify the template, e.g.:

.. code-block:: html+django

    {% load endless %}

    {% paginate objects %}
    {% for object in objects %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_pages %}

That's it!
If you want to display only previous and next links (in a page-by-page
pagination) you need to use the lower level ``get_pages`` templatetag
(see :doc:`templatetags_reference`),
e.g.:

.. code-block:: html+django

    {% load endless %}

    {% paginate objects %}
    {% for object in objects %}
        {# your code to show the entry #}
    {% endfor %}
    {% get_pages %}
    {{ pages.previous }} {{ pages.next }}

See :doc:`customization` that explains how to customize arrows
of previous and next pages.

Adding Ajax
~~~~~~~~~~~

The view is exactly the same as in ``show_more`` :doc:`twitter_pagination`::

    from endless_pagination.decorators import page_template

    @page_template('myapp/entry_index_page.html')  # just add this decorator
    def entry_index(
            request, template='myapp/entry_index.html', extra_context=None):
        context = {
            'objects': Entry.objects.all(),
        }
        if extra_context is not None:
            context.update(extra_context)
        return render_to_response(
            template, context, context_instance=RequestContext(request))

Of course you have to split templates, but this time a container for page
 template is needed too, and must have a class named *endless_page_template*.

*myapp/entry_index.html* becomes:

.. code-block:: html+django

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless.js"></script>
    {% endblock %}

    <h2>Entries:</h2>
    <div class="endless_page_template">
        {% include page_template %}
    </div>

*myapp/entry_index_page.html* becomes:

.. code-block:: html+django

    {% load endless %}

    {% paginate objects %}
    {% for object in objects %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_pages %}

Done.
