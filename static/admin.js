$(document).ready(function(){
    $('#updateSearchIndex').click(function(){
        var data = {};
        $.post('/admin/updateIndexes', data, function(response){
            alert('Indexes updated.')
        })
        .fail(function(){
            alert('Upload failed.');
        });
    });

    $('#doParse').click(function(){
        var data = {}
        data['input'] = $('#input').val();

        // get xml and display it
        data['type'] = 'xml';
        $.get('/admin/parse/doParse', data, function(responseData){
            writeXMLOutput(responseData);
        })
        .fail(function(){
            alert('Failed to retrieve XML data.');
        });

        // get string and display it
        data['type'] = 'string';
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

});

function clearAll(){
    $('#outputArea').empty();
    $('#stringArea').val('');
    $('#inputArea').val('');
}

function writeStringOutput(value){
    $('#stringArea').val(value);
}

function writeXMLOutput(xml){
    var domContainer = $('#outputArea');
    domContainer.empty();

    var xmlDoc = $.parseXML(xml);
    var list = $('<table></table>');
    $(xmlDoc).find('property')
        .each(function(){
            list.append('<tr><td>' + $(this).attr('name') + '</td><td>' + $(this).text() + '</td></tr>');
        });
    domContainer.append(list);
}