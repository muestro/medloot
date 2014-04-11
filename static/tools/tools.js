$(document).ready(function(){
    $('#calculateResult').click(function(){
        $('#result').empty();
        var data = {};
        data['moon'] = $('#moon').val();
        data['eclipse'] = $('#eclipse').val();
        data['full_text'] = $('#full_text').val();

        $.get('/tools/xpxp/calculate', data, function(responseData){
            if(responseData != "null"){
                //$('#result').empty().append(responseData);
                var response = $.parseJSON(responseData);
                $('#resultXPXP').empty().append(response.xpxp);
                $('#resultRemoveStorm').empty().append(response.remove_storm);
                $('#resultCreateRainstorm').empty().append(response.create_rainstorm);
                $('#resultLocateSerpents').empty().append(response.locate_serpents);
            }else{
                alert('Unable to parse data.');
            }

        }).fail(function(){
            alert('Unable to parse data.');
        });
    });
});