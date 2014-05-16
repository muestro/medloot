$(document).ready(function(){
    $('#calculateResult').click(function(){
        $('#result').empty();
        var data = {};
        data['moon'] = $('#moon').val();
        data['eclipse'] = $('#eclipse').val();
        data['full_text'] = $('#full_text').val();

        $.get('/tools/xpxp/calculate', data, function(responseData){
            if(responseData != "null"){
                var response = $.parseJSON(responseData);
                $('#resultXPXP').empty().append(response.xpxp);
                $('#resultRemoveStorm').empty().append(response.remove_storm);
                $('#resultCreateRainstorm').empty().append(response.create_rainstorm);
                $('#resultLocateSerpents').empty().append(response.locate_serpents);
                $('#debug').empty();
                $('#debug').append('Current time: ' + response.debug_current_time + '<br/>');
                $('#debug').append('Eclipse time: ' + response.debug_eclipse_time + '<br/>');
                $('#debug').append('<b>Next Solar Eclipse</b>: ' + response.debug_eclipse_time_diff + '<br/>');
                $('#debug').append('Moon time: ' + response.debug_moon_time + '<br/>');
                $('#debug').append('<b>Next New Moon</b>: ' + response.debug_moon_time_diff + '<br/>');
                $('.result').show();
            }else{
                alert('Unable to parse data.');
            }

        }).fail(function(){
            alert('Unable to parse data.');
        });
    });
});