$(document).ready(function(){
    // initializes links for ajax requests
    $("a.endless_more").live("click", function(){
        var container = $(this).closest(".endless_container");
        var loading = container.find(".endless_loading");
        $(this).hide();
        loading.show();
        $.get($(this).attr("href"), function(data){
            container.before(data);
            container.remove();
        });
        return false;
    });
    $("a.endless_page_link").live("click", function(){
        $(this).closest(".endless_page_template").load($(this).attr("href"));
        return false;
    }); 
});