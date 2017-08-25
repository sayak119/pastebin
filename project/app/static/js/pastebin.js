
$(document).ready(function() {
    $.ajax({
      url: 'http://127.0.0.1:8080/',
      type: 'POST',
      data: {},
      success: function(response){
        if(response.type == 1 && window.location == 'http://127.0.0.1:8080/')
          window.location = 'http://127.0.0.1:8080/create_paste' ;
        else if(response.type == 2 && window.location == 'http://127.0.0.1:8080/')
          window.location = 'http://127.0.0.1:8080/admin';
      },
      error: function(response){
        console.log(response);
      },
    });
});

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

//AJAX call for submitting paste
$(document).delegate('#submit_paste', 'click', function(e) {
  e.preventDefault();
  submitpaste($('#paste_code').val(),$('#post_input').val(),$('#datetimepicker').val(),$('#post_name').val(),$('#post_type').val());
});

var submitpaste = function(paste_code,lang,expire_time,title,type) {
  $.ajax({
    url:'http://127.0.0.1:8080/create_paste',
    type:'POST',
    data:{
      'title':title,
      'text':paste_code,
      'lang':lang,
      'time':expire_time,
      'type':type,
    },
    success:function (response) {
      red_url=response.url;
      window.location = "http://127.0.0.1:8080/"+red_url;
    },
    error:function(response) {
      console.log(response);
    }
  });
};
