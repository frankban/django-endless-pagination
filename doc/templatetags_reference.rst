Templatetags reference
======================

paginate
~~~~~~~~

Usage:

.. code-block:: html+django

    {% paginate objects %}

After this call, in the template context the *objects* variable is replaced
with only the objects of the current page.

You can also mantain your *objects* original variable (commonly a queryset)
and add to context another name referring to objects of the current page,
e.g.:

.. code-block:: html+django

    {% paginate objects as page_objects %}

The *as* argument is also useful when a nested context variable is provided
as queryset. In that case, and only in that case, the resulting variable
name is mandatory, e.g.:

.. code-block:: html+django

    {% paginate objects.all as objects %}

The number of paginated object is taken from settings, but you can
override the default, e.g.:

.. code-block:: html+django

    {% paginate 20 objects %}

Of course you can mix it all:

.. code-block:: html+django

    {% paginate 20 objects as paginated_objects %}

By default, the first page is displayed the first time you load the page,
but you can easily change this, e.g.:

.. code-block:: html+django

    {% paginate objects starting from page 3 %}

This can be also achieved using a template variable you passed in the
context, e.g.:

.. code-block:: html+django

    {% paginate objects starting from page page_number %}

If the passed page number does not exist then first page is displayed.

If you have multiple paginations in the same page, you can change the
querydict key for the single pagination, e.g.:

.. code-block:: html+django

    {% paginate objects using article_page %}

In this case *article_page* is intended to be a context variable, but you can
hardcode the key using quotes, e.g.:

.. code-block:: html+django

    {% paginate objects using 'articles_at_page' %}

Again, you can mix it all (the order of arguments is important):

.. code-block:: html+django

    {% paginate 20 objects starting from page 3 using page_key as paginated_objects %}

Additionally you can pass a path to be used for the pagination:

.. code-block:: html+django

    {% paginate 20 objects using page_key with pagination_url as paginated_objects %}

This way you can easily create views acting as API endpoints and point your
Ajax calls to that API. In this case *pagination_url* is considered a
context variable, but it is also possible to hardcode the url, e.g.:

.. code-block:: html+django

    {% paginate 20 objects with "/mypage/" %}

If you want the first page to contain a different number of items than
subsequent pages you can separate the two values with a comma, e.g. if
you want 3 items on the first page and 10 on other pages:

.. code-block:: html+django

    {% paginate 3,10 objects %}

You must use this tag before calling the `show_more`_ one.

lazy_paginate
~~~~~~~~~~~~~

Paginate objects without hitting the database with a *select count* query.

Use this the same way as `paginate`_ tag when you are not interested
in the total number of pages.

show_more
~~~~~~~~~

Show the link to get the next page in a :doc:`twitter_pagination`.
Usage:

.. code-block:: html+django

    {% show_more %}

Alternatively you can override the label passed to the default template:

.. code-block:: html+django

    {% show_more "even more" %}

You can override the loading text too:

.. code-block:: html+django

    {% show_more "even more" "working" %}

Must be called after `paginate`_ or `lazy_paginate`_.

get_pages
~~~~~~~~~

Usage:

.. code-block:: html+django

    {% get_pages %}

This is mostly used for :doc:`digg_pagination`.
This call inserts in the template context a *pages* variable, as a sequence
of page links. You can use *pages* in different ways:

just print *pages* and you will get Digg-style pagination displayed:

.. code-block:: html+django

    {{ pages }}

display pages count:

.. code-block:: html+django

    {{ pages|length }}

get a specific page:

.. code-block:: html+django

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

iterate over *pages* to get all pages:

.. code-block:: html+django

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

You can change the variable name, e.g.:

.. code-block:: html+django

    {% get_pages as page_links %}

Must be called after `paginate`_ or `lazy_paginate`_.

show_pages
~~~~~~~~~~

Show page links.
Usage:

.. code-block:: html+django

    {% show_pages %}

It is only a shortcut for:

.. code-block:: html+django

    {% get_pages %}
    {{ pages }}

You can set ``ENDLESS_PAGINATION_PAGE_LIST_CALLABLE`` in your *settings.py*
as a callable used to customize the pages that are displayed.
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

If ``ENDLESS_PAGINATION_PAGE_LIST_CALLABLE`` is *None* an internal
callable is used, generating a Digg-style pagination.

Must be called after `paginate`_ or `lazy_paginate`_.

show_current_number
~~~~~~~~~~~~~~~~~~~

Show (or insert in the context) the current page number.
This tag can be useful for example to change page title according to
current page number.
To just show current page number:

.. code-block:: html+django

    {% show_current_number %}

If you use multiple paginations in the same page you can get the page
number for a specific pagination using the querystring key, e.g.:

.. code-block:: html+django

    {% show_current_number using mykey %}

Default page when no querystring is specified is 1. If you changed it in the
`paginate`_ template tag, you have to call  ``show_current_number``
according to your choice, e.g.:

.. code-block:: html+django

    {% show_current_number starting from page 3 %}

This can be also achieved using a template variable you passed in the
context, e.g.:

.. code-block:: html+django

    {% show_current_number starting from page page_number %}

Of course, you can mix it all (the order of arguments is important):

.. code-block:: html+django

    {% show_current_number starting from page 3 using mykey %}

If you want to insert the current page number in the context, without
actually displaying it in the template, use the *as* argument, i.e.:

.. code-block:: html+django

    {% show_current_number as page_number %}
    {% show_current_number starting from page 3 using mykey as page_number %}
