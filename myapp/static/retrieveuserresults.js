var wordlimit = 150; //TODO fix this for each question
var getResults = function (qid, qname) {
    console.log(qid, qname);
    var url = "/getanswerforuser/";
    var he = highlightErrors;
    $('#question').text(qname);
    $.post(url, {"qid":qid}, function (data) {
        console.log(data);
        $('#w_c').text(data['wordCount']);
        $('#grammar').text(data['grammarErrorCount']);
        $('#spelling').text(data['spellingErrorCount']);
        if (data['wordCount'] >= wordlimit) {
            $('#wordlimit').text("Met");
            $('#score').text(data['score']);

        } else {
            $('#wordlimit').text("Failed");
            $('#score').text('0');
        }
        he(data["answer"], data["errors"]);
        $('#essay').show();
        $('#res').show();
        $('#myModal').modal('show');
    }, "json")
}