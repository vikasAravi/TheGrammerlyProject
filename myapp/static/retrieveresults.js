var wordlimit = 150; //TODO fix this for each question
var getResults = function (uid) {
    var round = function(v) {
        return Math.round(v * 100)/100
    }
    var qid = window.location.href;
    qid = qid.substring(qid.lastIndexOf('/')+1);
    var url = "/getresult/";
    $('#username').text(uid);
    $.post(url, {"uid":uid, "qid":qid}, function (data) {
        $('#w_c').text(data['wordCount']);
        $('#grammar').text(data['grammarErrorCount']);
        $('#spelling').text(data['spellingErrorCount']);
        $('#wordlimit').text(round(data['wordlimitpenalty']));
        $('#score').text(round(data['score']));
        $('#sentencequality').text(round(data['sentencequalitypenalty']));
        $('#wordquality').text(round(data['wordqualitypenalty']));
        highlightErrors(data["answer"], data["errors"]);
        $('#essay').show();
        $('#res').show();
        $('#myModal').modal('show');
    }, "json")
}