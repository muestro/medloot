$(document).ready(function(){
    $('.resultItem').click(function(){
        $('.selected').removeClass('selected');
        $(this).addClass('selected');

        var itemNum = $(this).attr('itemNum');
        var sourceValue = $('#sourceStringData' + itemNum).val();
        var stringValue = $('#resultItemStringData' + itemNum).val();
        var xmlValue = $('#resultItemXMLData' + itemNum).val();

        $('#displaySourceArea').val(sourceValue);
        $('#displayStringArea').val(stringValue);
        $('#displayXMLArea').val(xmlValue);
    });
});

