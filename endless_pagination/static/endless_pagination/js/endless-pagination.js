(function ($) {
    'use strict';

    $.fn.endlessPaginate = function(options) {
        var defaults = {
            // Twitter-style pagination link selector.
            moreSelector: 'a.endless_more',
            // Digg-style pagination link selector.
            pagesSelector: 'a.endless_page_link',
            // Set this to true to use the paginate-on-scroll feature.
            paginateOnScroll: false,
            // If paginate-on-scroll is on, this margin will be used.
            paginateOnScrollMargin : 1,
            // Callback called when the user clicks to get another page.
            onClick: function() {},
            // Callback called when the requested data is loaded.
            onLoaded: function() {},
            // Callback called when the new page is correctly displayed.
            onCompleted: function() {}
        },
            settings = $.extend(defaults, options);

        var getData = function(link) {
            return 'querystring_key=' + link.attr('rel').split(' ')[0];
        };

        return this.each(function() {
            var element = $(this);
            // Twitter-style pagination.
            element.find(settings.moreSelector).live('click', function() {
                var link = $(this),
                    container = link.closest('.endless_container');
                link.hide();
                container.find('.endless_loading').show();
                $.get(link.attr('href'), getData(link), function(data) {
                    container.before(data);
                    container.remove();
                });
                return false;
            });
            // Digg-style pagination.
            element.find(settings.pagesSelector).live('click', function() {
                var link = $(this),
                    page_template = link.closest('.endless_page_template');
                page_template.load(link.attr('href'), getData(link));
                return false;
            });
        });
    };

    $.endlessPaginate = function(options) {
        return $('body').endlessPaginate(options);
    };

})(jQuery);
