
var wordlimit = 150;

var submitEssay = function (e) {
    //TODO: decide about word limit
    clearInterval(timer);
    $('#loader').show();
    let text = $('#id_answer').val();
    let qid = $('#myqid').text();
    let starttime = $('#starttime').text();
    console.log(qid);
    $.post(
        '/fetch/',
        {
            'essay': text,
            'qid': qid,
            'starttime':starttime
        },
        function (data) {
            $('#w_c').text(data['wordCount']);
            $('#grammar').text(data['grammarErrorCount']);
            $('#spelling').text(data['spellingErrorCount']);
            if (data['wordCount'] >= wordlimit) {
                $('#wordlimit').text("Met");
                $('#score').text(data['score']);

            } else {
                $('#wordlimit').text("Failed");
                $('#score').text(0);
            }
            $("#submit_button").attr("disabled", true);
            highlightErrors(text, data["errors"]);
            $('#id_answer').hide();
            $('#submit_button').hide();
            $('#wordcount').hide();
            $('#essay').show();
            $('#res').show();
            $('#loader').hide();
        }, "json"
    )
}

$('#submit_button').click(submitEssay);

//TIMER Functionality begins
var timelimit = 1800; // in seconds
var starttime = new Date().getTime();

var pad = function (num, size) {
    var s = num + "";
    while (s.length < size) s = "0" + s;
    return s;
}

var updateTimer = function () {
    var t = new Date();
    var timeinsec = timelimit - Math.floor((t.getTime() - starttime) / 1000);
    var timeinmin = Math.floor(timeinsec / 60);
    var actualsec = (timeinsec - timeinmin * 60);
    $('#time').text("Time : " + pad(timeinmin, 2) + " : " + pad(actualsec, 2));
    if (timeinsec == 0) {
        clearInterval(timer);
        submitEssay();
        console.log("time over");
    }

}

var timer = setInterval(updateTimer, 1000);
//Timer functionality ends

function wordCount(val) {
    var wom = val.match(/\S+/g);
    return {
        words: (wom ? wom.length : 0)
    };
}

window.onbeforeunload = function (e) {
    return ''
}

var textarea = document.getElementById("id_answer");
var result = document.getElementById("wordcount");
textarea.addEventListener("input", function () {
    var v = wordCount(this.value);
    result.innerHTML = (
        v.words + " words"
    );
}, false);

