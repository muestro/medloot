$(document).ready(function(){
    $('#updateSearchIndex').click(function(){
        var data = {};
        $.post('/admin/updateIndexes', data, function(response){
            alert('Indexes updated.');
            location.reload();
        })
        .fail(function(){
            alert('Upload failed.');
            location.reload();
        });
    });

    $('#addAdminButton').click(function(){
        $('#addAdminButton').prop( "disabled", true );
        var data = {};
        data['alias'] = $('#addAdminAlias').val();
        data['email'] = $('#addAdminEmail').val();
        $.post('/admin/addadmin', data, function(){
            setTimeout(function(){
                location.reload();
            }, 500);
        })
        .fail(function(){
            alert('Failed to add Admin.');
        });
    });

    $('#editItemButton').click(function(){
        var itemKey = $('#itemKeyInput').val();
        window.location.href = '/admin/item?item_key=' + itemKey;
    });

    $('#doParse').click(function(){
        var data = {};
        data['input'] = $('#input').val();

        // get string and display it
        $.get('/admin/parse/doParse', data, function(responseData){
            writeStringOutput(responseData);
        })
        .fail(function(){
            alert('Failed to retrieve string data.');
        });
    });

    $('#upload').click(function(){
        var data = {};
        data['input'] = $('#input').val();
        $.post('/admin/parse/upload', data, function(response){
            alert('Successfully uploaded.');
            clearAll();
        })
        .fail(function(){
            alert('Upload failed.');
        });
    });

    // update the date fields values of the local time
    $('[dateValue]').each(function(){
        var utcTime = $(this).attr('dateValue');
        var localDateTime = new Date(utcTime);
        $(this).append(localDateTime.toLocaleString());
    });

    $('[message]').each(function(){
        var message = $(this).attr('message');
        $(this).append(message);
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
