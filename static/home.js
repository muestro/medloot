$(document).ready(function(){
    $("#searchBar").keyup(function(event){
        if(event.keyCode == 13){
            $("#searchIcon").click();
            return false;
        }
    });

    $('#searchIcon').click(function(){
        window.location.href = '/search?q=' + encodeURIComponent($('#searchBar').val());
    });

});