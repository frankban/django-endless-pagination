Changelog
=========

Version 1.2 (under development)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**New feature**: the ``page_templates`` decorator also accepts a sequence
of ``(template, key)`` pairs, functioning as a dict mapping templates and
keys (still present), e.g.::

    from endless_pagination.decorators import page_templates

    @page_templates((
        ('myapp/entries_page.html', None),
        ('myapp/other_entries_page.html', 'other_objects_page'),
    ))
    def entry_index():
        ...

This also supports serving different paginated objects with the same template.

----

**New feature**: ability to provide nested context variables in the
*paginate* and *lazy_paginate* template tags, e.g.:

.. code-block:: html+django

    {% paginate objects.all as myobjects %}

The code above is basically equivalent to:

.. code-block:: html+django

    {% with objects.all as myobjects %}
        {% paginate myobjects %}
    {% endwith %}

In this case, and only in this case, the `as` argument is mandatory, and a
*TemplateSyntaxError* will be raised if the variable name is missing.

----

**New feature**: ability to create a development and testing environment
(see :doc:`contributing`).

----

**New feature**: in addition to the ability to provide a customized pagination
URL as a context variable, the *paginate* and *lazy_paginate* tags now
support hardcoded pagination URL endpoints, e.g.:

.. code-block:: html+django

    {% paginate 20 objects with "/mypage/" %}

----

**Documentation**: general clean up.

----

**Documentation**: added a :doc:`contributing` page. Have a look!

----

**Fix**: ``endless_pagination.views.AjaxListView`` no longer subclasses
``django.views.generic.list.ListView``. Instead, the base objects and
mixins composing the final view are now defined by this app.

This change eliminates the ambiguity of having two separate pagination
machineries in place: the Django Endless Pagination one and the built-in
Django ``ListView`` one.

----

**Fix**: the *using* argument of *paginate* and *lazy_paginate* template tags
now correctly handles querystring keys containing dashes, e.g.:

.. code-block:: html+django

    {% lazy_paginate entries using "entries-page" %}

----

**Fix**: in some corner cases, loading ``endless_pagination.models`` raised
an *ImproperlyConfigured* error while trying to pre-load the templates.

----

**Fix**: replaced doctests with proper unittests. Improved the code coverage
as a consequence. Also introduced integration tests exercising Javascript,
based on Selenium.

----

**Fix**: overall code lint and clean up.


Version 1.1
~~~~~~~~~~~

**New feature**: now it is possible to set the bottom margin used for
pagination on scroll (default is 1 pixel).

For example, if you want the pagination on scroll to be activated when
20 pixels remain until the end of the page:

.. code-block:: html+django

    <script src="http://code.jquery.com/jquery-latest.js"></script>
    <script src="{{ STATIC_URL }}endless_pagination/js/endless.js"></script>
    <script src="{{ STATIC_URL }}endless_pagination/js/endless_on_scroll.js"></script>

    {# add the lines below #}
    <script type="text/javascript" charset="utf-8">
        var endless_on_scroll_margin = 20;
    </script>

----

**New feature**: added ability to avoid Ajax requests when multiple pagination
is used.

A template for multiple pagination with Ajax support may look like this
(see :doc:`multiple_pagination`):

.. code-block:: html+django

    {% block js %}
        {{ block.super }}
        <script src="http://code.jquery.com/jquery-latest.js"></script>
        <script src="{{ STATIC_URL }}endless_pagination/js/endless.js"></script>
    {% endblock %}

    <h2>Entries:</h2>
    <div class="endless_page_template">
        {% include "myapp/entries_page.html" %}
    </div>

    <h2>Other entries:</h2>
    <div class="endless_page_template">
        {% include "myapp/other_entries_page.html" %}
    </div>

But what if you need Ajax pagination for *entries* but not for *other entries*?
You will only have to add a class named ``endless_page_skip`` to the
page container element, e.g.:

.. code-block:: html+django

    <h2>Other entries:</h2>
    <div class="endless_page_template endless_page_skip">
        {% include "myapp/other_entries_page.html" %}
    </div>

----

**New feature**: implemented a class-based generic view allowing
Ajax pagination of a list of objects (usually a queryset).

Intended as a substitution of *django.views.generic.ListView*, it recreates
the behaviour of the *page_template* decorator.

For a complete explanation, see :doc:`generic_views`.

----

**Fix**: the ``page_template`` and ``page_templates`` decorators no longer
hide the original view name and docstring (*update_wrapper*).

----

**Fix**: pagination on scroll now works on Firefox >= 4.

----

**Fix**: tests are now compatible with Django 1.3.
