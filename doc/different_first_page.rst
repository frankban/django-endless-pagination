Different number of items on the first page
===========================================

Sometimes you might want to show on the first page a different number of
items than subsequent pages (e.g. in a movie detail page you want to show
4 images of the movie as a reminder, letting the user click to see other 20
images, and so on). This is easy to achieve using comma separated first page
and per page arguments, e.g.:

.. code-block:: html+django

    {% load endless %}
    
    {% lazy_paginate 4,20 objects %}
    {% for object in objects %}
        {# your code to show the entry #}
    {% endfor %}
    {% show_more %}
    
This code will display 4 objects on the first page and 20 objects on the other
pages.
