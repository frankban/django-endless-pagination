Getting current page number
===========================

In the template
~~~~~~~~~~~~~~~

You can get and display the current page number in the template using
the ``show_current_number`` templatetag, e.g.:

.. code-block:: html+django

    {% show_current_number %}

The previous call will display the current page number, but you can also
insert the value in the context as a template variable:

.. code-block:: html+django


    {% show_current_number as page_number %}
    {{ page_number }}

See :doc:`templatetags_reference` for more information on
``show_current_number`` accepted arguments.

In the view
~~~~~~~~~~~

If you need to get the current page number in the view, you can use an utility
function called ``get_page_number_from_request``, e.g.::

    from endless_pagination import utils

    page = utils.get_page_number_from_request(request)

If you are using multiple pagination or you have changed the default
querystring for pagination, you can pass the querystring key as
an optional argument::

    page = utils.get_page_number_from_request(request, querystring_key=mykey)

If the page number is not present in the request, by default *1* is returned.
You can change this behaviour using::

    page = utils.get_page_number_from_request(request, default=3)

