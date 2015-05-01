function hideRows(rows, isActive){
    rows.each(function(index){
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
}

$(document).ready(function(){
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

    // dynamic filter building
    $('.dynamicFilterGroup').each(function(){
        var buttonGroupContainer = $(this).find('.filterButtonGroup');
        var valueSet = {};
        var filterGroupValue = $(this).attr('filterGroupValue');
        $('td[filterGroup="' + filterGroupValue + '"][hasData]').each(function(){
            // if it has a value, add it to our filter set
            var value = $(this).attr("filter");
            if(value && value != "" && !(value in valueSet)) {
                valueSet[value] = true;
            }
        });
        // setup each of the filter button groups
        $.each(Object.keys(valueSet), function(index, value){
            buttonGroupContainer.append('<button statFilterButton filter="' + value + '">' + value + '</button>');
        });
        if (Object.keys(valueSet).length > 0){
            $(this).css('display', 'table-row');
        }
    });

    var filterButtons = $("button[filter]");

    filterButtons.filter('[statFilterButton]').click(function() {
        $(this).toggleClass("active");
        var isActive = $(this).hasClass('active');

        var filter = $(this).attr('filter');
        var rowsToHide = $('td[filter="' + filter + '"]:not([hasData])').closest('tr');

        hideRows(rowsToHide, isActive);
    });

    filterButtons.filter('[classFilterButton]').click(function() {
        $(this).toggleClass("active");
        var isActive = $(this).hasClass('active');

        var filterText = $(this).attr('filter');
        var rowsToHide = $("span:contains(" + filterText + ")").filter('.lit').parents('tr.resultRow');

        hideRows(rowsToHide, isActive);
    });

    filterButtons.filter('[numberFilterButton]').click(function() {
        $(this).toggleClass("active");
        var isActive = $(this).hasClass('active');

        var filter = $(this).attr('filter');
        var rowsToHide = $('td.statBlock[filter="' + filter + '"]:not([hasData])').closest('tr');

        hideRows(rowsToHide, isActive);
    });

    filterButtons.filter('[equipableLocationFilterButton]').click(function(){
        $(this).toggleClass("active");
        var isActive = $(this).hasClass('active');

        var filter = $(this).attr('filter');
        var rowsToHide = $('td[filter="equipableLocation"]').filter(function (){
            return $(this).text().indexOf(filter) == -1;
        }).parents('tr.resultRow');

        hideRows(rowsToHide, isActive);
    });
});