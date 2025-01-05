// AUTOCOMPLETE ON SEARCH NODE
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

// RESIZING TEXT AREAS DYNAMICALLY
function autoResizeTextArea(textarea) {
    textarea.style.height = 'auto'; // Reset height to auto to calculate correct scrollHeight
    textarea.style.height = `${textarea.scrollHeight}px`; // Set the height based on scrollHeight
}