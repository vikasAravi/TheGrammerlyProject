
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



var timer; 
//Timer functionality ends

function wordCount(val) {
    var wom = val.match(/\S+/g);
    return {
        words: (wom ? wom.length : 0)
    };
}

var textarea;
var result;


$(function() {
    textarea =  document.getElementById("id_answer");
    result = document.getElementById("wordcount");
    timelimit = parseInt($('#time').text())*60;
    wordlimit = parseInt($('#wordcount').text());
    //console.log(timelimit, wordlimit);
    timer = setInterval(updateTimer, 1000);
    textarea.addEventListener("input", function () {
        var v = wordCount(this.value);
        var str = v.words + " words (" + wordlimit + ")"
        var f;
        if(v.words < wordlimit) {
            f = str.fontcolor('red');
        } else {
            f = str.fontcolor('green');
        }
        result.innerHTML = f;
    }, false);

    $( window ).unload(function() {
        return 'Think before you leave! You will lose all your content and you will have to re-write again.';
    });
})