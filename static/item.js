google.setOnLoadCallback(drawChart);
function drawChart() {
    /*
    var data = google.visualization.arrayToDataTable([
        ['Age', 'Weight'],
        [8, 0],
        [4, 0],
        [11, 0],
        [4, 0],
        [3, 0],
        [37, 0]
    ]);
    */

    var options = {
        title: '',
        hAxis: {title: '', minValue: 0, maxValue: 15},
        vAxis: {title: '', minValue: 0, maxValue: 0, gridlines: {count: 0}},
        legend: 'none'
    };

    $('li[key]').each(function(index) {
        var keyValue = $(this).attr("key");

        // build up the dataset that google needs
        var data = [];
        data.push(['', '']);
        $(this).find('input[name="' + keyValue + '"]').each(function(index) {
            data.push([parseInt($(this).attr('value')), 0])
        });

        var googleData = google.visualization.arrayToDataTable(data);
        var chart = new google.visualization.ScatterChart(document.getElementById('chart_div_' + keyValue));
        chart.draw(googleData, options);
    });
}