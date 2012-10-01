Multiple pagination in the same page
====================================

Sometimes it is necessary to show different types of paginated objects in the
same page. In this case we have to associate to every pagination a different
querystring key.
Normally, the key used is the one specified in
``settings.ENDLESS_PAGINATION_PAGE_LABEL`` (see :doc:`customization`),
but in the case of multiple pagination the application provides a simple way to
override the settings.
If you do not need AJAX, the only file you need to edit
is the template. Here is a usecase example with 2 different paginations
(*objects* and *other_objects*) in the same page, but there is no limit to the
number of different paginations in a page:

.. code-block:: html+django

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

The ``using`` argument of the ``paginate`` template tag allows you to choose the
name of the querystring key used to track the page number.
If not specified the system falls back to ``settings.ENDLESS_PAGINATION_PAGE_LABEL``.
In the example above, the url *http://example.com?page=2&other_objects_page=3*
requests the second page of *objects* and the third page of *other_objects*.

The name of the querystring key can also be dinamically passed in the template
context, e.g.:

.. code-block:: html+django

    {% paginate other_objects using page_variable %} {# <-- page_variable is not surrounded by quotes #}

You can use any style of pagination: ``show_pages``, ``get_pages``, ``show_more``
etc... (see :doc:`templatetags_reference`).

Adding AJAX for multiple pagination
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Obviously each pagination needs a template for the page content.
Remember to box each page in a div with a class called *endless_page_template*.

*myapp/entry_index.html*:

.. code-block:: html+django

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

*myapp/entries_page.html*:

.. code-block:: html+django

    {% load endless %}

    {% paginate objects %}
    {% for object in objects %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_pages %}

*myapp/other_entries_page.html*:

.. code-block:: html+django

    {% load endless %}

    {% paginate other_objects using other_objects_page %}
    {% for object in other_objects %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_pages %}

Again the decorator ``page_template`` simplifies the management of AJAX requests
in views. You must, however, map different paginations to different page templates.
You can chain decorator's calls relating a template with the associated
querystring key, e.g.::

    from endless_pagination.decorators import page_template

    @page_template('myapp/entries_page.html')
    @page_template('myapp/other_entries_page.html', key='other_objects_page')
    def entry_index(
            request, template='myapp/entry_index.html', extra_context=None):
        context = {
            'objects': Entry.objects.all(),
            'other_objects': OtherEntry.objects.all(),
        }
        if extra_context is not None:
            context.update(extra_context)
        return render_to_response(
            template, context, context_instance=RequestContext(request))

As seen in previous examples, if you do not specify the *key* kwarg in the
decorator, then the page template is associated to the querystring key
defined in the settings.

You can use the ``page_templates`` (note the trailing *s*) decorator in
substitution of a decorator's chain when you need multiple AJAX pagination.
The previous example can be written::

    from endless_pagination.decorators import page_templates

    @page_templates({
        'myapp/entries_page.html': None,
        'myapp/other_entries_page.html': 'other_objects_page',
    })
    def entry_index():
        ...

As seen, a dict object is passed to the ``page_templates`` decorator, mapping
templates to querystring keys. Alternatively, you can also pass a sequence
of ``(template, key)`` pairs, e.g.::

    from endless_pagination.decorators import page_templates

    @page_templates((
        ('myapp/entries_page.html', None),
        ('myapp/other_entries_page.html', 'other_objects_page'),
    ))
    def entry_index():
        ...

This way the use case of different paginated objects being served by the
same template is also supported.


Manually select what to bind
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What if you need AJAX pagination for *entries* but not for *other entries*?
You will only need to add a class named ``endless_page_skip`` to the
page container element, e.g.:

.. code-block:: html+django

    <h2>Other entries:</h2>
    <div class="endless_page_template endless_page_skip">
        {% include "myapp/other_entries_page.html" %}
    </div>
