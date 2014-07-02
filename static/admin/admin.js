$(document).ready(function(){
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
