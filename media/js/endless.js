$(document).ready(function(){
    // initializes links for ajax requests
    $(".endless_more").live("click", function(){
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
});