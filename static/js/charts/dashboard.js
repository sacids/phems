//charts
var options = {
    series: [30, 70],
    chart: {
        type: "donut",
        height: 260,
    },
    labels: ["Approved", "Pending"],
    colors: ["#388E3C", "#f1b44c"],
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

//pending and approval total
// $.getJSON('api/dashboard/consent-percentage', (data) => {
//     if (data.error == false) {
//         //charts
//         var options = {
//             series: [data.approved, data.pending],
//             chart: {
//                 type: "donut",
//                 height: 260,
//             },
//             labels: ["Approved", "Pending"],
//             colors: ["#388E3C", "#f1b44c"],
//             legend: {
//                 show: !1
//             },
//             plotOptions: {
//                 pie: {
//                     donut: {
//                         size: "70%"
//                     }
//                 }
//             }
//         };
//         //render chart
//         var chart = new ApexCharts(document.querySelector("#pending-approve-chart"), options);
//         chart.render()
//     }
// });



// //pending and approved mandate
// $.getJSON('api/dashboard/consent-value', (data) => {
//     if (data.error == false) {
//         var arrApproved = [];
//         var arrPending = [];

//         for (k = 0; k < data.data_array.length; k++) {
//             arrPending.push(data.data_array[k].pending);
//             arrApproved.push(data.data_array[k].approved);
//         }

//         var options = {
//             series: [{
//                 name: "Approved",
//                 data: arrApproved
//             },
//             {
//                 name: "Pending",
//                 data: arrPending
//             }
//             ],
//             chart: {
//                 height: 320,
//                 type: "line",
//                 toolbar: "false",
//                 dropShadow: {
//                     enabled: !0,
//                     color: "#000",
//                     top: 18,
//                     left: 7,
//                     blur: 8,
//                     opacity: .2
//                 }
//             },
//             dataLabels: {
//                 enabled: !1
//             },
//             colors: ["#388E3C", "#f1b44c"],
//             stroke: {
//                 curve: "smooth",
//                 width: 3
//             }
//         },
//             chart = new ApexCharts(document.querySelector("#line-chart"), options);
//         chart.render();
//     }
// });

// //pending and approved by payment channel
// $.getJSON('api/dashboard/consent-per-channel', (data) => {
//     if (data.error == false) {

//         var arrChannels = [];
//         var arrApproved = [];
//         var arrPending = [];

//         for (k = 0; k < data.data_array.length; k++) {
//             arrChannels.push(data.data_array[k].name);
//             arrPending.push(data.data_array[k].pending);
//             arrApproved.push(data.data_array[k].approved);
//         }

//         //charts
//         var options = {
//             series: [{
//                 name: "Approved",
//                 data: arrApproved
//             }, {
//                 name: "Pending",
//                 data: arrPending
//             }],
//             chart: {
//                 type: 'bar',
//                 height: 320,
//             },
//             plotOptions: {
//                 bar: {
//                     borderRadius: 4,
//                     horizontal: true,
//                     dataLabels: {
//                         position: 'bottom'
//                     },
//                 }
//             },
//             dataLabels: {
//                 enabled: false
//             },
//             xaxis: {
//                 categories: arrChannels,
//             },
//             labels: ["Approved", "Pending"],
//             colors: ["#388E3C", "#f1b44c"],
//         };

//         var chart = new ApexCharts(document.querySelector("#bar-chart"), options);
//         chart.render();
//     }
// });

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

