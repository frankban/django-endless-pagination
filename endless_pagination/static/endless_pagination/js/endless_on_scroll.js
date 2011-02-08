(function($) {
    $(document).ready(function(){
        $(window).scroll(function(){
        	if ($(window).scrollTop() == $(document).height() - $(window).height()) {
        	    $("a.endless_more").click();
        	}
        });
    });
})(jQuery);
