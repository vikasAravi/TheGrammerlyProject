var wordlimit = 150; //TODO fix this for each question
var getResults = function (qid, qname) {
    var round = function(v) {
        return Math.round(v * 100)/100
    };
    var url = "/getanswerforuser/";
    $('#question').text(qname);
    $.post(url, {"qid":qid}, function (data) {
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
};