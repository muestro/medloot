$(document).ready(function(){
    $('#calculateResult').click(function(){
        $('#result').empty();
        var data = {};
        data['moon'] = $('#moon').val();
        data['eclipse'] = $('#eclipse').val();
        data['full_text'] = $('#full_text').val();

        $.get('/tools/xpxp/calculate', data, function(responseData){
            if(responseData != "None"){
                $('#result').empty().append(responseData);
            }else{
                alert('Unable to parse data.');
            }

        }).fail(function(){
            alert('Unable to parse data.');
        });
    });
});