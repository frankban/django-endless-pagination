Digg-style pagination
=====================

Digg-style pagination of queryset objects is really easy to implement. If Ajax
pagination is not needed, all you have to do is modifying the template, e.g.:

.. code-block:: html+django

    {% load endless %}

    {% paginate entries %}
    {% for entry in entries %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_pages %}

That's it!

If you only want to display previous and next links (in a page-by-page
pagination) you have to use the lower level ``get_pages`` templatetag
(see :doc:`templatetags_reference`),
e.g.:

.. code-block:: html+django

    {% load endless %}

    {% paginate entries %}
    {% for entry in entries %}
        {# your code to show the entry #}
    {% endfor %}
    {% get_pages %}
    {{ pages.previous }} {{ pages.next }}

:doc:`customization` explains how to customize the arrows that go to previous
and next pages.

The ``{% get_pages %}`` template tag adds to the current template context a
``pages`` variable containing several methods that can be used to fully
customize how the page links are displayed. For example, assume you want to
show the indexes of the entries in the current page, followed by the total
number of entries:

.. code-block:: html+django

    {% load endless %}

    {% paginate entries %}
    {% for entry in entries %}
        {# your code to show the entry #}
    {% endfor %}
    {% get_pages %}
    Showing entries
    {{ pages.current_start_index }}-{{ pages.current_end_index }} of
    {{ pages.total_count }}.
    {# Just print pages to render the Digg-style pagination. #}
    {{ pages }}

Again, for a full overview of the ``get_pages`` template tag, see
:doc:`templatetags_reference`.

Adding Ajax
~~~~~~~~~~~

The view is exactly the same as in ``show_more`` from
:doc:`twitter_pagination`::

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

Of course you have to split templates, as seen in :doc:`twitter_pagination`,
but this time a container for the page template is needed too and, by default,
must have a class named *endless_page_template*.

*myapp/entry_index.html* becomes:

.. code-block:: html+django

    <h2>Entries:</h2>
    <div class="endless_page_template">
        {% include page_template %}
    </div>

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
    {% show_pages %}

Done.

It is possible to manually override the container selector used by
*$.endlessPaginate()* to update the page contents. This can be easily achieved
by customizing the *pageSelector* option of *$.endlessPaginate()*, e.g.:

.. code-block:: html+django

    <h2>Entries:</h2>
    <div id="entries">
        {% include page_template %}
    </div>

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless-pagination.js"></script>
        <script>$.endlessPaginate({pageSelector: 'div#entries'});</script>
    {% endblock %}

See the :doc:`javascript` for a detailed explanation of how to integrate
JavaScript and Ajax features in Django Endless Pagination.
