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
});

