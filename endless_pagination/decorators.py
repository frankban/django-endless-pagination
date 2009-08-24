def page_template(template):
    """
    Decorate a view that takes a *template* and *extra_context* keyword
    arguments (like generic views).
    The template is switched to *page_template* if request is ajax.
    The name of the page template is given as *page_template* in the
    extra context.
    """
    def decorator(view):
        # decorator with arguments wrap      
        def decorated(request, *args, **kwargs):
            # trust the developer: he wrote context.update(extra_context) in his view
            extra_context = kwargs.setdefault("extra_context", {})
            extra_context['page_template'] = template
            # switch template on ajax requests
            if request.is_ajax():
                kwargs['template'] = template
            return view(request, *args, **kwargs)
        return decorated
    return decorator