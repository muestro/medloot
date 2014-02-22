$(document).ready(function(){
    $(".resultRow").click(function(){
        var displayRow = $('#displayRow' + $(this).attr("rowNum"));
        if(displayRow.is(":visible")){
            displayRow.hide();
        }else{
            displayRow.show();
        }
    });
});