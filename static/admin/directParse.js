$(document).ready(function() {
    $('#parseButton').click(function () {
        var data = {};
        data['input'] = $('#input').val().substring(0,10000);

        // get string and display it
        $.post('/admin/parse/direct/doParse', data)
        .done(function(data){
            window.location.replace('/admin/parse/direct/' + data);
        })
        .fail(function () {
            alert('Failed /admin/parse/direct/doParse operation.');
        });
    });
});