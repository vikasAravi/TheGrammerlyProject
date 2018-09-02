//this is for context of testcreator view of a particular user
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

uuid=0

$(function() {
    $('#minscore').change(function() {
        $('#maxscore').attr("min", $(this).val())
    });

    $('#maxscore').change(function() {
        $('#minscore').attr("max", $(this).val())
    });

    $('#modChart').on('shown.bs.modal',function(event){
        // Chart initialisieren
        var modal = $(this);
        var canvas = modal.find('.modal-body canvas');
        var ctx = canvas[0].getContext("2d");
        $.getJSON("/getuserperfdata/" + uuid, function (data) {
            //load chart based on data
            var myBarChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels:data['labels'],
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
                            gridLines: { display: false },
                            ticks: { display: false }
                        }]
                    }
                }
            });
        });
    }).on('hidden.bs.modal',function(event){
        // reset canvas size
        var modal = $(this);
        var canvas = modal.find('.modal-body canvas');
        canvas.attr('width','568px').attr('height','300px');
        // destroy modal
        $(this).data('bs.modal', null);
    });
})

var showUserChart = function (uid, uname) {
    $('#username').text(uname);
    uuid = uid;
    $('#modChart').modal('show');
}

