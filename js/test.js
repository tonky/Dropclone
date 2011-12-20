$(document).ready(function() {
    $(".del").click(function() {
        var file_div = $(this).parent();

        var file_id = file_div.attr("id");

        $.post('/del/'+file_id, function(data) {
            file_div.remove();
        });
    });
});
