$(document).ready(function(){
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
});