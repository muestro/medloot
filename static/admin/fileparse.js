$(document).ready(function(){
    $('.resultItem').click(function(){
        $('.selected').removeClass('selected');
        $(this).addClass('selected');

        var itemNum = $(this).attr('itemNum');
        var stringValue = $('#resultItemStringData' + itemNum).val();
        var xmlValue = $('#resultItemXMLData' + itemNum).val();

        $('#displayStringArea').val(stringValue);
        $('#displayXMLArea').val(xmlValue);
    });
});

