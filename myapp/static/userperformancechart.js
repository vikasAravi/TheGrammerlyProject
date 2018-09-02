$(document).ready(function () {
    $.getJSON("/getuserattemptdata/", function (data) {
        //load chart based on data
        var ctx = document.getElementById("myChart").getContext('2d');
        
        var myBarChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels:data['labels'],
                lineColor:'red',
                datasets: [{
                    data: data['data'],
                    borderColor: "#8e5ea2",
                    backgroundColor: "#8e5ea222"
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
                        gridLines: { display: false },
                        ticks: { display: false }
                    }]
                }
            }
        });
    })
})