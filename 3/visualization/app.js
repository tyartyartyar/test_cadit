Highcharts.chart('container', {
    chart: {
        type: 'spline'
    },
    title: {
        text: 'Temperature Live Data'
    },

    data: {
        csvURL: 'http://localhost:1234',
        enablePolling: true
    }
});
