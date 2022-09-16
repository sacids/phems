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
                    pointFormat: '<td style="padding:0"><b>{point.y:,.0f}</b></td></tr>',
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
                    name: 'Events',
                    colorByPoint: true,
                    data: [
                        {
                            name: "On Progress",
                            y: data.on_progress
                        },
                        {
                            name: "Discarded",
                            y: data.discarded
                        },
                        {
                            name: "Closed",
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

    //events per sector
    $.getJSON("event-sectors-chart", (data) => {
        if (data.error == false) {
            var arrSectors = [];
            var arrNew = [];
            var arrProgress = [];
            var arrClosed = [];
            var arrDiscarded = [];

            for (k = 0; k < data.chart.length; k++) {
                arrSectors.push(data.chart[k].name);
                arrNew.push(data.chart[k].new);
                arrProgress.push(data.chart[k].progress);
                arrClosed.push(data.chart[k].closed);
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
                    headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                    pointFormat: '<td style="padding:0"><b>{point.y:,.0f}</b></td></tr>',
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
                    name: 'Closed',
                    color: "#388E3C",
                    data: arrClosed
                }],
                credits: {
                    enabled: false
                }
            });
        }//error false
    });





});