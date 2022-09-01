//pending and approval total
$.getJSON('percent-rate-chart', (data) => {
    if (data.error == false) {
        //charts
        var options = {
            series: [data.success, data.discarded],
            chart: {
                type: "donut",
                height: 260,
            },
            labels: ["Approved", "Discarded"],
            colors: ["#388E3C", "#B71C1C"],
            legend: {
                show: !1
            },
            plotOptions: {
                pie: {
                    donut: {
                        size: "70%"
                    }
                }
            }
        };
        //render chart
        var chart = new ApexCharts(document.querySelector("#pending-approve-chart"), options);
        chart.render()
    }
});

//channel
$.getJSON('channel-rate-chart', (data) => {
    if (data.error == false) {
        var arrChannels = [];
        var arrNew = [];
        var arrSuccess = [];
        var arrDiscarded = [];

        for (k = 0; k < data.chart.length; k++) {
            arrChannels.push(data.chart[k].name);
            arrNew.push(data.chart[k].new);
            arrSuccess.push(data.chart[k].success);
            arrDiscarded.push(data.chart[k].discarded);
        }

        //charts
        var options = {
            series: [{
                name: "New signals",
                data: arrNew
            }, {
                name: "Approved",
                data: arrSuccess
            },
            {
                name: "Discarded",
                data: arrDiscarded
            }
            ],
            chart: {
                type: 'bar',
                height: 320,
            },
            plotOptions: {
                bar: {
                    borderRadius: 4,
                    horizontal: true,
                    dataLabels: {
                        position: 'bottom'
                    },
                }
            },
            dataLabels: {
                enabled: false
            },
            xaxis: {
                categories: arrChannels,
            },
            labels: ["New signals","Approved", "Discarded"],
            colors: ["#1565C0", "#388E3C", "#B71C1C"],
        };

        var chart = new ApexCharts(document.querySelector("#channel-rate-chart"), options);
        chart.render();
    }
});

//percentage rate of events
$.getJSON('event-percent-chart', (data) => {
    if (data.error == false) {
        //charts
        var options = {
            series: [data.closed, data.discarded],
            chart: {
                type: "donut",
                height: 260,
            },
            labels: ["Closed", "Discarded"],
            colors: ["#388E3C", "#B71C1C"],
            legend: {
                show: !1
            },
            plotOptions: {
                pie: {
                    donut: {
                        size: "70%"
                    }
                }
            }
        };
        //render chart
        var chart = new ApexCharts(document.querySelector("#event-percent-chart"), options);
        chart.render()
    }
});

//events
$.getJSON('event-sectors-chart', (data) => {
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

        //charts
        var options = {
            series: [{
                name: "New events",
                data: arrNew
            }, {
                name: "On Progress",
                data: arrProgress
            },
            {
                name: "Discarded",
                data: arrDiscarded
            },
            {
                name: "Closed",
                data: arrClosed
            }
            ],
            chart: {
                type: 'bar',
                height: 320,
            },
            plotOptions: {
                bar: {
                    borderRadius: 4,
                    horizontal: true,
                    dataLabels: {
                        position: 'bottom'
                    },
                }
            },
            dataLabels: {
                enabled: false
            },
            xaxis: {
                categories: arrSectors,
            },
            labels: ["New events","On Progress", "Discarded", "Closed"],
            colors: ["#1565C0", "#F57C00", "#B71C1C", "#388E3C"],
        };

        var chart = new ApexCharts(document.querySelector("#event-sectors-chart"), options);
        chart.render();
    }
});



