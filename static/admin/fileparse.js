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
                    valueString = valueString.replace(/ None/g, ' "None"');
                    valueString = valueString.replace(/ True/g, ' "True"');
                    valueString = valueString.replace(/ False/g, ' "False"');

                    try {
                        value = JSON.parse(valueString);
                    }catch(err){
                        $('#error').append('Error when JSON.parse(): ' + err.message +
                            '<br/>item: ' + $('#resultItem'+$(element).attr('editForItem')).text().trim() +
                            '<br/>key: ' + key +
                            '<br/>value string: ' + valueString +
                            '<br/><br/>');
                        // continue to the next iteration
                        return true;
                    }
                }else{
                    if(!isNaN(valueString)){
                        valueString = parseInt(valueString);
                    }

                    if(valueString == "True"){
                        valueString = true;
                    }

                    if(valueString == "False"){
                        valueString = false;
                    }

                    value = valueString;
                }

                if(value != "None"){
                    if($.isArray(value)){
                        // check to see if any of the inner values in the object needs to convert to pure booleans
                        $.each(value, function(index, obj){
                            if($.isArray(obj) || $.isPlainObject(obj)){
                                $.each(obj, function(propName, propValue){
                                    if(propValue == "True"){
                                        value[index][propName] = true;
                                    }else if(propValue == "False"){
                                        value[index][propName] = false;
                                    }else if(propValue == "None"){
                                        value[index][propName] = false;
                                    }
                                });
                            }
                        });
                    }

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

