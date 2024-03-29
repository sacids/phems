$(document).ready(function () {
    //highcharts options
    Highcharts.setOptions({
        lang: {
            thousandsSep: ','
        }
    });

    //event percentage rate
    $.getJSON("event-percent-chart", (data) => {
        if (data.error == false) {
            $('#event-percent-chart').highcharts({
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie',
                    backgroundColor: '#FAFAFA'
                },
                title: {
                    text: ""
                },
                legend: {
                    enabled: true,
                    floating: false,
                    verticalAlign: 'bottom',
                    align: 'center',
                    layout: 'horizontal'
                },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                },
                tooltip: {
                    headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                    pointFormat: '<td style="padding:0"><b>{point.y:,.1f}%</b></td></tr>',
                    footerFormat: '</table>',
                    shared: true,
                    useHTML: true
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        colors: [
                            '#1565C0',
                            '#F57C00',
                            '#B71C1C',
                            '#388E3C',
                        ],
                        dataLabels: {
                            enabled: true,
                            format: '{point.percentage:.1f} %',
                            distance: 0
                        },
                        showInLegend: true,
                        point: {
                            events: {
                                legendItemClick: function (e) {
                                    e.preventDefault();
                                }
                            }
                        }
                    }
                },
                series: [{
                    name: 'Events',
                    colorByPoint: true,
                    data: [
                        {
                            name: "New",
                            y: data.new
                        },
                        {
                            name: "On Progress",
                            y: data.on_progress
                        },
                        {
                            name: "Discarded",
                            y: data.discarded
                        },
                        {
                            name: "Confirmed",
                            y: data.confirmed
                        }
                    ]
                }],
                credits: {
                    enabled: false
                }
            });
        }//error false
    });

    //events per sector
    $.getJSON("event-sectors-chart", (data) => {
        if (data.error == false) {
            var arrSectors = [];
            var arrNew = [];
            var arrProgress = [];
            var arrConfirmed = [];
            var arrDiscarded = [];

            for (k = 0; k < data.chart.length; k++) {
                arrSectors.push(data.chart[k].name);
                arrNew.push(data.chart[k].new);
                arrProgress.push(data.chart[k].progress);
                arrConfirmed.push(data.chart[k].confirmed);
                arrDiscarded.push(data.chart[k].discarded);
            }

            //channel rate chart
            $('#event-sectors-chart').highcharts({
                chart: {
                    type: 'line',
                    backgroundColor: '#FAFAFA'
                },
                title: {
                    text: null
                },
                xAxis: {
                    categories: arrSectors,
                    crosshair: true
                },
                yAxis: {
                    title: {
                        text: null
                    }
                },
                tooltip: {
                    headerFormat: '<span style="font-size:12px; font-weight: bold;">{point.key}</span><table>',
                    pointFormat: '<tr><td style="padding:0;"> <i>{series.name}:</i> </td>' +
                        '<td style="padding:0"><b> {point.y:,.0f}</b></td></tr>',
                    footerFormat: '</table>',
                    shared: true,
                    useHTML: true
                },
                plotOptions: {
                    column: {
                        pointPadding: 0.2,
                        borderWidth: 0,
                        dataLabels: {
                            enabled: true,
                            style: {
                                fontWeight: 'bold'
                            }
                        }
                    }
                },
                series: [{
                    name: 'On Progress',
                    color: "#F57C00",
                    data: arrProgress
                },
                {
                    name: 'Discarded',
                    color: "#B71C1C",
                    data: arrDiscarded
                },
                {
                    name: 'Confirmed',
                    color: "#388E3C",
                    data: arrConfirmed
                }],
                credits: {
                    enabled: false
                }
            });
        }//error false
    });

    //alert charts
    $.getJSON("alert-event-chart", (data) => {
        if (data.error == false) {
            var arrName = [];
            var arrEvent = [];
            var arrConfirmedEvent = [];

            for (k = 0; k < data.chart.length; k++) {
                arrName.push(data.chart[k].name);
                arrEvent.push(data.chart[k].number_of_events)
                arrConfirmedEvent.push(data.chart[k].confirmed_events)
            }

            $('#alert-event-chart').highcharts({
                chart: {
                    type: 'column',
                    backgroundColor: '#FAFAFA'
                },
                title: {
                    text: null
                },
                xAxis: {
                    categories: arrName,
                    crosshair: true
                },
                yAxis: {
                    title: {
                        text: null
                    }
                },
                tooltip: {
                    headerFormat: '<span style="font-size:12px; font-weight: bold;">{point.key}</span><table>',
                    pointFormat: '<tr><td style="padding:0;"> <i>{series.name}:</i> </td>' +
                        '<td style="padding:0"><b> {point.y:,.0f}</b></td></tr>',
                    footerFormat: '</table>',
                    shared: true,
                    useHTML: true
                },
                plotOptions: {
                    column: {
                        pointPadding: 0.2,
                        borderWidth: 0,
                        dataLabels: {
                            enabled: true,
                            style: {
                                fontWeight: 'bold'
                            }
                        }
                    }
                },
                series: [{
                    name: 'Number of Events',
                    color: "#1565C0",
                    data: arrEvent
                },
                {
                    name: 'Confirmed Events',
                    color: "#2E7D32",
                    data: arrConfirmedEvent
                }],
                credits: {
                    enabled: false
                }
            });
        }//error false
    });


    //signal percentage rates
    $.getJSON("percent-rate-chart", (data) => {
        if (data.error == false) {
            $('#signal-percent-chart').highcharts({
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie',
                    backgroundColor: '#FAFAFA'
                },
                title: {
                    text: ""
                },
                legend: {
                    enabled: true,
                    floating: false,
                    verticalAlign: 'bottom',
                    align: 'center',
                    layout: 'horizontal'
                },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                },
                tooltip: {
                    headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                    pointFormat: '<td style="padding:0"><b> {point.y:,.1f}%</b></td></tr>',
                    footerFormat: '</table>',
                    shared: true,
                    useHTML: true
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        colors: [
                            '#F57C00',
                            '#B71C1C',
                            '#388E3C',
                        ],
                        dataLabels: {
                            enabled: true,
                            format: '{point.percentage:.1f} %',
                            distance: 0
                        },
                        showInLegend: true,
                        point: {
                            events: {
                                legendItemClick: function (e) {
                                    e.preventDefault();
                                }
                            }
                        }
                    }
                },
                series: [{
                    name: 'Signal (Alert)',
                    colorByPoint: true,
                    data: [
                        {
                            name: "Pending",
                            y: data.pending
                        },
                        {
                            name: "Discarded",
                            y: data.discarded
                        },
                        {
                            name: "Approved",
                            y: data.success
                        }
                    ]
                }],
                credits: {
                    enabled: false
                }
            });
        }//error false
    });


    //channel-rate-chart
    $.getJSON("channel-rate-chart", (data) => {
        if (data.error == false) {
            var arrChannel = [];
            var arrNew = [];
            var arrSuccess = [];
            var arrDiscarded = [];

            for (k = 0; k < data.chart.length; k++) {
                arrChannel.push(data.chart[k].name);
                arrNew.push(data.chart[k].new);
                arrSuccess.push(data.chart[k].success);
                arrDiscarded.push(data.chart[k].discarded);
            }

            //channel rate chart
            $('#channel-rate-chart').highcharts({
                chart: {
                    type: 'line',
                    backgroundColor: '#FAFAFA'
                },
                title: {
                    text: null
                },
                xAxis: {
                    categories: arrChannel,
                    crosshair: true
                },
                yAxis: {
                    title: {
                        text: null
                    }
                },
                tooltip: {
                    headerFormat: '<span style="font-size:12px; font-weight: bold;">{point.key}</span><table>',
                    pointFormat: '<tr><td style="padding:0;"> <i>{series.name}:</i> </td>' +
                        '<td style="padding:0"><b> {point.y:,.0f}</b></td></tr>',
                    footerFormat: '</table>',
                    shared: true,
                    useHTML: true
                },
                plotOptions: {
                    column: {
                        pointPadding: 0.2,
                        borderWidth: 0,
                        dataLabels: {
                            enabled: true,
                            style: {
                                fontWeight: 'bold'
                            }
                        }
                    }
                },
                series: [{
                    name: 'New',
                    color: "#F57C00",
                    data: arrNew
                },
                {
                    name: 'Discarded',
                    color: "#B71C1C",
                    data: arrDiscarded
                },
                {
                    name: 'Approved',
                    color: "#388E3C",
                    data: arrSuccess
                }],
                credits: {
                    enabled: false
                }
            });
        }//error false
    });





});