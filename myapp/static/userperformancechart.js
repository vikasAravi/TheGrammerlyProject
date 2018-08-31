$(document).ready(function () {
    $.getJSON("/getuserattemptdata/", function (data) {
        //load chart based on data
        var ctx = document.getElementById("myChart").getContext('2d');
        var myBarChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    data: data['data']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            min: 0,
                            max: 10
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'score'
                        }
                    }],
                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'time'
                        }
                    }]
                }
            }
        });
    })
})