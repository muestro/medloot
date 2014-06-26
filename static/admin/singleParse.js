$(document).ready(function() {
    $('#doParse').click(function () {
        var data = {};
        data['input'] = $('#input').val();

        // get string and display it
        $.get('/admin/singleParse/doParse', data, function (responseData) {
            writeStringOutput(responseData);
        })
            .fail(function () {
                alert('Failed to retrieve string data.');
            });
    });

    $('#upload').click(function () {
        var data = {};
        data['input'] = $('#input').val();
        $.post('/admin/singleParse/upload', data, function (response) {
            alert('Successfully uploaded.');
            clearAll();
        })
            .fail(function () {
                alert('Upload failed.');
            });
    });
});


function clearAll(){
    $('#outputArea').empty();
    $('#stringArea').val('');
    $('#inputArea').val('');
}

function writeStringOutput(value){
    $('#stringArea').val(value);
}
