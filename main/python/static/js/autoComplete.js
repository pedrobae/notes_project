$(function() {
    $("#searchNode").autocomplete({
        source:function(request, response) {
            $.getJSON("/autocomplete", {
                q: request.term,
            }, function(data) {
                response(data.matching_results);
            });
        },
        minLength: 2,
        select: function(event, ui) {
            console.log(ui.item.value); 
        }
    });
});