$(document).ready(function(){
    $("#searchBar").keyup(function(event){
        if(event.keyCode == 13){
            $("#searchIcon").click();
            return false;
        }
    });

    $('#searchIcon').click(function(){
        window.location.href = '/search2?q=' + encodeURIComponent($('#searchBar').val());
    });
});