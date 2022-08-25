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

// //on CLICK 
// $('#select-month').on('change', function (e) {
//     e.preventDefault;

//     //variables
//     var monthName = $(this).val();

//     $.getJSON('api/dashboard/consent-per-channel', { month: monthName }, (data) => {
//         if (data.error == false) {

//             var arrChannels = [];
//             var arrApproved = [];
//             var arrPending = [];

//             for (k = 0; k < data.data_array.length; k++) {
//                 arrChannels.push(data.data_array[k].name);
//                 arrPending.push(data.data_array[k].pending);
//                 arrApproved.push(data.data_array[k].approved);
//             }

//             //charts
//             var options = {
//                 series: [{
//                     name: "Approved",
//                     data: arrApproved
//                 }, {
//                     name: "Pending",
//                     data: arrPending
//                 }],
//                 chart: {
//                     type: 'bar',
//                     height: 320,
//                 },
//                 plotOptions: {
//                     bar: {
//                         borderRadius: 4,
//                         horizontal: true,
//                         dataLabels: {
//                             position: 'bottom'
//                         },
//                     }
//                 },
//                 dataLabels: {
//                     enabled: false
//                 },
//                 xaxis: {
//                     categories: arrChannels,
//                 },
//                 labels: ["Approved", "Pending"],
//                 colors: ["#388E3C", "#f1b44c"],
//             };

//             var chart = new ApexCharts(document.querySelector("#bar-chart"), options);
//             chart.render();
//         }
//     });

// });

