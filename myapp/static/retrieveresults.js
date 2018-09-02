var wordlimit = 150; //TODO fix this for each question
var getResults = function (uid) {
    var qid = window.location.href;
    qid = qid.substring(qid.lastIndexOf('/')+1);
    var url = "/getresult/";
    $('#username').text(uid);
    console.log(url);
    var he = highlightErrors;
    $.post(url, {"uid":uid, "qid":qid}, function (data) {
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