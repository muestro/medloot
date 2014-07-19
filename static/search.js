$(document).ready(function(){
    // fill in the dynamic filters
    // equipable location
    var container = $("#equipableLocationFilterGroup");
    var equipableLocationSet = {};
    $('td[filter="equipableLocation"]').each(function(){
        var locations = $.trim($(this).text()).split(" ");
        $.each(locations, function(index, value){
             if(value != "" && !(value in equipableLocationSet)){
                equipableLocationSet[value] = true;
             }
        });
    });

    // setup each of the filter button groups
    $.each(Object.keys(equipableLocationSet), function(index, value){
        container.append('<button equipableLocationFilterButton filter="' + value + '">' + value + '</button>');
    });

    $("button[filter]").filter('[classFilterButton]').click(function() {
        $(this).toggleClass("active");
        var isActive = $(this).hasClass('active');

        var filterText = $(this).attr('filter');
        var rowsToHide = $("span:contains(" + filterText + ")").filter('.lit').parents('tr.resultRow');

        rowsToHide.each(function(index){
            var hideCount = 0;
            if (this.hasAttribute('hideCount')){
                hideCount = parseInt($(this).attr('hideCount'));
            }

            if(isActive){
                $(this).hide();
                hideCount += 1;
                $(this).attr('hideCount', hideCount);
            }else{
                hideCount -= 1;
                if(hideCount == 0){
                    $(this).show();
                }
                $(this).attr('hideCount', hideCount);
            }
        });

    });

    $("button[numberFilterButton]").click(function(){
        $(this).toggleClass("active");
        var isActive = $(this).hasClass('active');

        var filter = $(this).attr('filter');
        var rowsToHide = $('td.statBlock[filter="' + filter + '"]').not(':has(span)').parents('tr.resultRow');

        rowsToHide.each(function(index){
            var hideCount = 0;
            if (this.hasAttribute('hideCount')){
                hideCount = parseInt($(this).attr('hideCount'));
            }

            if(isActive){
                $(this).hide();
                hideCount += 1;
                $(this).attr('hideCount', hideCount);
            }else{
                hideCount -= 1;
                if(hideCount == 0){
                    $(this).show();
                }
                $(this).attr('hideCount', hideCount);
            }
        });
    });

    $("button[equipableLocationFilterButton]").click(function(){
        $(this).toggleClass("active");
        var isActive = $(this).hasClass('active');

        var filter = $(this).attr('filter');
        var rowsToHide = $('td[filter="equipableLocation"]').filter(function (){
            return $(this).text().indexOf(filter) == -1;
        }).parents('tr.resultRow');

        rowsToHide.each(function(index){
            var hideCount = 0;
            if (this.hasAttribute('hideCount')){
                hideCount = parseInt($(this).attr('hideCount'));
            }

            if(isActive){
                $(this).hide();
                hideCount += 1;
                $(this).attr('hideCount', hideCount);
            }else{
                hideCount -= 1;
                if(hideCount == 0){
                    $(this).show();
                }
                $(this).attr('hideCount', hideCount);
            }
        });
    });
});