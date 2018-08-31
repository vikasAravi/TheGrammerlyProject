
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

var showError = function (errorText, errorJSON) {
    var tooltip = errorJSON['message'] + "\nSuggestions:";

    for (var i = 0; i < errorJSON.suggestions.length; i++) {
        tooltip += "\n" + errorJSON.suggestions[i];
    }

    var tag = "span";
    if (errorText.trim().length == 0) {
        tag = "pre";
    }
    var x =
        "<" + tag + " class='error "
        + errorJSON.type
        + "' data-toggle='tooltip'"
        + " title='" + tooltip
        + "'>"
        + errorText
        + "</" + tag + ">";

    return x;
}

var showText = function (text) {
    return "<span class='correct'>" + text + "</span>";
}

var appendElem = function (e, html) {
    e.append($(html));
}

var highlightErrors = function (text, errors) {
    if (errors.length == 0) return;

    var offset = errors[0].offset;
    var length;
    var e = $('#essay');

    if (offset > 0) {
        appendElem(e, showText(text.substring(0, offset)));
    }

    for (var i = 0; i < errors.length; i++) {
        offset = errors[i].offset;
        length = errors[i].length;
        console.log(offset, length);
        appendElem(e, showError(
            text.substring(offset, offset + length),
            errors[i]
        ));

        if (i == errors.length - 1) {
            appendElem(e, showText(text.substring(offset + length)));
        } else {
            appendElem(e, showText(text.substring(offset + length, errors[i + 1].offset)));
        }
    }
}
