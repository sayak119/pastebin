$(document).ready(function() {
    $('#report_link').click(function() {
        window.location = window.location.href + '/add_report';
        return false;
    });
});

$(document).ready(function() {
    $('#edit_link').click(function() {
        window.location = window.location.href + '/edit';
        return false;
    });
});

$(document).ready(function() {
    $('#embed_link').click(function() {
        window.location = window.location.href + '/embed/output';
        return false;
    });
});


$(document).ready(function() {
    $('#print_link').click(function() {
        window.print();
        return false;
    });
});

var confirm_delete = function(){
    if(confirm('Are You Sure You Want To Delete This Paste?') == true)
    {
        delete_post();
    }
    return;
};

$(document).delegate('#delete_link', 'click', function(e) {
    e.preventDefault();
    confirm_delete()
});


var delete_post = function() {
    $.ajax({
        url: "http://127.0.0.1:8080" + window.location.pathname + "/delete",
        type: 'POST',
        // async: false,
        success: function(response) {
            if(response.user_type == 1)
                window.location = "http://127.0.0.1:8080/create_paste";
            else
                window.location = "http://127.0.0.1:8080/admin"

        },
        error: function(response) {
            console.log(response);
            window.location.reload();
        }
    });
};

function saveTextAsFile() {
    var textToWrite = $('#paste_code_raw').text();
    var textFileAsBlob = new Blob([textToWrite], { type: 'text/plain' });
    var fileNameToSaveAs = $("#title").html().substring($("#title").html().lastIndexOf(" ") + 1) + "." +  $("#language").html().substring($("#language").html().lastIndexOf(" ") + 1);

    var downloadLink = document.createElement("a");
    downloadLink.download = fileNameToSaveAs;
    downloadLink.innerHTML = "Download File";
    var link = document.createElement("a");
    if (link.download !== undefined) { // feature detection
        // Browsers that support HTML5 download attribute
        link.setAttribute("href", window.URL.createObjectURL(textFileAsBlob));
        link.setAttribute("download", fileNameToSaveAs);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}


$(document).ready(function() {
    var button = document.getElementById('save_link');
    button.addEventListener('click', saveTextAsFile);
});


// function destroyClickedElement(event) {
//     // remove the link from the DOM
//     document.body.removeChild(event.target);
// }

$(document).ready(function() {
    $.ajax({
        url: "http://127.0.0.1:8080" + "/api" + window.location.pathname,
        type: 'POST',
        success: function(response) {
            console.log(response);
            // $('#info').html("Title : "+response.paste_title+"  Owner : "+response.paste_owner+"  Language : "+response.paste_lang+"  Expiry Details : "+response.paste_expire);
            $('#title').html("Title : " + response.paste_title);
            document.title = 'View Paste : '+response.paste_title;
            $('#owner').html("Owner : " + response.paste_owner);
            $('#language').html("Language : " + response.paste_lang);
            $('#paste_code_raw').text(response.paste_text);
            // highlightCodeTemp = response.paste_text.replace("<", "&lt;");
            // highlightCode = highlightCodeTemp.replace(">", "&gt;");
            $('#highlighted_paste').text(response.paste_text);
            $('#highlighted_paste').attr("class", response.paste_lang);
            $('pre code').each(function(i, block) {
                hljs.highlightBlock(block);
            });
        },
        error: function(response) {
            console.log(response);
        }
    });
});