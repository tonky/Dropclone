$(document).ready(function() {
    var $dialog = $('<div></div>')
        .html('Email: <input type="text" id="email_address"/><br/>Message: <input type="text" id="message"/>(optional)')
        .dialog({
            autoOpen: false,
            title: 'Send file link',
            width: 400,
            buttons: [{text: 'Share', click:
                function() {
                    $.post('/mail/',
                        { "user_email": $("#email_address").val(), "file_id": "bb", "message": ""},
                        function(data) {
                            console.log(data);
                            $dialog.dialog('close');
                    });
            }}]
        });

    $(".share").click(function() {
        $dialog.dialog('open');
    });

    $(".del").click(function() {
        var file_div = $(this).parent();

        var file_id = file_div.attr("id");

        $.post('/del/'+file_id, function(data) {
            file_div.remove();
        });
    });
});
