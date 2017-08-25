$(document).delegate('#reg_submit', 'click', function(e) {
  e.preventDefault();
  register_user($('#reg_username').val(),$('#reg_email').val(),$('#reg_pass').val(),$('#reg_passcheck').val());
});

function validateEmail(email) 
{
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

var register_user = function(username,email,password,password_check) {
  if(validateEmail(email))
  {
    if(password == password_check){
      $.ajax({
        url:"http://127.0.0.1:8080/register",
        type:'POST',
        data:{
          'username':username,
          'email':email,
          'password':password,
        },
        success:function (response) {
        console.log(response);
        window.location = "http://127.0.0.1:8080/login";
        },
        error:function (response) {
          alert(response.responseJSON.error);
        }
      });
    }
    else {
        //document.getElementById("reg_passcheck").style.borderColor = "red";
        alert("Re-Password doesnt match the Password");
    }
  }
  else
  {
    alert("Enter an valid E-mail Address");
    //document.getElementById("reg_email").innerHTML = "blabla";
  }  
};
