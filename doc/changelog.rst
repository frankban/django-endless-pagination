Changelog
=========

Version 1.1
~~~~~~~~~~~

**New feature**: now it is possible to set the bottom margin used for
pagination on scroll (default is 1 pixel).

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
    
----

**New feature**: added ability to avoid AJAX requests when multiple pagination
is used.

A template for multiple pagination with AJAX support may look like this 
(see :doc:`multiple_pagination`):

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

But what if you need AJAX pagination for *entries* but not for *other entries*?
You will only need to add a class named ``endless_page_skip`` to the 
page container element, e.g.:

.. code-block:: html+django

    <h2>Other entries:</h2>
    <div class="endless_page_template endless_page_skip">
        {% include "myapp/other_entries_page.html" %}
    </div>

----

**New feature**: implemented a class based generic view allowing
AJAX pagination of a list of objects (usually a queryset).

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
