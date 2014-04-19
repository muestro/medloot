$(document).ready(function(){
    $('.resultItem').click(function(){
        $('.selected').removeClass('selected');
        $(this).addClass('selected');

        var itemNum = $(this).attr('itemNum');

        $('.outputItem').hide();
        $('#outputItem' + itemNum).show();
    });

    $('.editLink').click(function(){
        var itemNum = $(this).attr('itemNum');
        $('#outputItem' + itemNum + ' .editItem').show();
        return false;
    });

    $('#upload').click(function(){
        // get list of checked items
        var data = {};

        var itemList = [];
        $('input:checked').each( function( index, element ){
            var itemNum = $(this).attr('itemNum');
            // get all the inputs that are of this item num
            var dict = {};
            $('input[editForItem="' + itemNum + '"]').each( function(index, element){
                var key = $(this).attr('key');
                var valueString = $(this).val();
                var value;
                if(valueString.indexOf('[') == 0){
                    valueString = valueString.replace(/'/g, '"');
                    value = JSON.parse(valueString);
                }else{
                    value = valueString;
                }

                if(value != "None"){
                    dict[key] = value;
                }
            });
            itemList.push(dict);
        });

        data["items"] = JSON.stringify(itemList);

        $.post('/admin/fileParse/upload', data, function(response){
            alert(response);
            window.location.href = "/admin"
        })
        .fail(function(){
            alert('Upload failed.');
        });
    });
});

