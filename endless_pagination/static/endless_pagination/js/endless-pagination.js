(function ($) {
    'use strict';

    $.fn.endlessPaginate = function(options) {
        var defaults = {
            // Twitter-style pagination container selector.
            containerSelector: '.endless_container',
            // Twitter-style pagination loading selector.
            loadingSelector: '.endless_loading',
            // Twitter-style pagination link selector.
            moreSelector: 'a.endless_more',
            // Digg-style pagination page template selector.
            pageSelector: '.endless_page_template',
            // Digg-style pagination link selector.
            pagesSelector: 'a.endless_page_link',
            // Callback called when the user clicks to get another page.
            onClick: function() {},
            // Callback called when the new page is correctly displayed.
            onCompleted: function() {},
            // Set this to true to use the paginate-on-scroll feature.
            paginateOnScroll: false,
            // If paginate-on-scroll is on, this margin will be used.
            paginateOnScrollMargin : 1
        },
            settings = $.extend(defaults, options);

        var getContext = function(link) {
            return {
                querystring_key: link.attr('rel').split(' ')[0],
                url: link.attr('href')
            };
        };

        return this.each(function() {
            var element = $(this);

            // Twitter-style pagination.
            element.find(settings.moreSelector).live('click', function() {
                var link = $(this),
                    html_link = link.get(0),
                    container = link.closest(settings.containerSelector),
                    loading = container.find(settings.loadingSelector);
                // Avoid multiple Ajax calls.
                if (loading.is(':visible')) {
                    return false;
                }
                link.hide();
                loading.show();
                var context = getContext(link);
                // Fire onClick callback.
                if (settings.onClick.apply(html_link, [context]) !== false) {
                    var data = 'querystring_key=' + context.querystring_key;
                    // Send the Ajax request.
                    $.get(context.url, data, function(fragment) {
                        container.before(fragment);
                        container.remove();
                        // Fire onCompleted callback.
                        settings.onCompleted.apply(
                            html_link, [context, fragment]);
                    });
                }
                return false;
            });

            // On scroll pagination.
            if (settings.paginateOnScroll) {
                var win = $(window),
                    doc = $(document);
                win.scroll(function(){
                    if (doc.height() - win.height() -
                        win.scrollTop() <= settings.paginateOnScrollMargin) {
                        element.find(settings.moreSelector).click();
                    }
                });
            }

            // Digg-style pagination.
            element.find(settings.pagesSelector).live('click', function() {
                var link = $(this),
                    html_link = link.get(0),
                    context = getContext(link);
                // Fire onClick callback.
                if (settings.onClick.apply(html_link, [context]) !== false) {
                    var page_template = link.closest(settings.pageSelector),
                        data = 'querystring_key=' + context.querystring_key;
                    // Send the Ajax request.
                    page_template.load(context.url, data, function(fragment) {
                        // Fire onCompleted callback.
                        settings.onCompleted.apply(
                            html_link, [context, fragment]);
                    });
                }
                return false;
            });
        });
    };

    $.endlessPaginate = function(options) {
        return $('body').endlessPaginate(options);
    };

})(jQuery);
