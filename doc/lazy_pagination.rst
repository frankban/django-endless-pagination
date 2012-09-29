Lazy pagination
===============

Usually pagination requires to hit the database to get the total number of items
to display. Lazy pagination avoids this *select count* query and results in a
faster page load, with a disadvantage: you can't know the total number of pages.
For this reason it is better to use lazy pagination in conjunction with
twitter-style pagination (e.g. using the ``show_more`` template tag).

To switch to lazy pagination all you have to do is to use the
``{% lazy_paginate %}`` template tag instead of the ``{% paginate %}`` one, e.g.:

.. code-block:: html+django

    {% load endless %}

    {% lazy_paginate objects %}
    {% for object in objects %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_more %}

The ``lazy_paginate`` tag can take all the args of ``paginate``
(see :doc:`templatetags_reference`).
