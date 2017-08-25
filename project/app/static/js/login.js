$(document).delegate('#login_submit', 'click', function(e) {
  e.preventDefault();
  user_login($('#user_name').val(),$('#pass').val());
});

var user_login = function(username,password) {
  $.ajax({
    url:"http://127.0.0.1:8080/login",
    type:'POST',
    data:{
      'username':username,
      'password':password,
    },
    // async: false,
    success:function (response){
      console.log(response);
      if(response.type == 1)
        window.location = "http://127.0.0.1:8080/create_paste";
      else
        window.location = "http://127.0.0.1:8080/admin"
    },
    error:function (response) {
      console.log(response);
      alert(response.responseJSON.error);
    }
  });
};
