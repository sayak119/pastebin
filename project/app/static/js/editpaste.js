function selectPasteContent() {
    $('#paste_code').select();
}

$(document).delegate('#paste_code', 'keydown', function(e) {
    var keyCode = e.keyCode || e.which;

    if (keyCode == 9) {
        e.preventDefault();
        var start = $(this).get(0).selectionStart;
        var end = $(this).get(0).selectionEnd;

        // set textarea value to: text before caret + tab + text after caret
        $(this).val($(this).val().substring(0, start) + "\t" + $(this).val().substring(end));

        // put caret at right position again
        $(this).get(0).selectionStart =
            $(this).get(0).selectionEnd = start + 1;
    }
});

// $(document).ready(function() {
//     var code = $(".codemirror-textarea")[0];
//     var editor = CodeMirror.fromTextArea(code, {
//         lineNumbers: true
//     });
// });

//AJAX call for submitting paste
$(document).delegate('#edit_paste', 'click', function(e) {
  e.preventDefault();
  submitpaste($('#paste_code').val(),$('#post_input').val(),$('#datetimepicker').val(),$('#post_name').val(),$('#post_type').val());
});


$(document).ready(function(){
  path = window.location.pathname;
  $.ajax({
    url: "http://127.0.0.1:8080" + "/api" + path.substring(0,path.length- 5),
    type: 'POST',
    success: function(response){
      console.log(response);
      $('#paste_code').val(response.paste_text);
      $('#datetimepicker').val(response.paste_expire);
      $('#post_name').val(response.paste_title);
      $("option[value='response.paste_lang']").attr('selected','selected');
    },
    error: function(response){
      console.log(response);
    },
  });
});

var submitpaste = function(paste_code,lang,expire_time,title,type) {
  $.ajax({
    url: window.location,
    type: 'POST',
    data:{
      'title':title,
      'text':paste_code,
      'lang':lang,
      'time':expire_time,
      'type':type,
    },
    success:function (response) {
      red_url=response.url;
      console.log(red_url);
      window.location = "http://127.0.0.1:8080/"+red_url;
    },
    error:function(response) {
      console.log(response);
    }
  });
};
