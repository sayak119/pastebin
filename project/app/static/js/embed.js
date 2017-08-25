$(document).ready(function(){
	path = window.location.href;
	str = path.substring(0,path.length - 7);
	console.log(str);
	ele = document.getElementById('embed_out');
	ele.innerText = "<script src= \"" +  str + "\" ></script>";
});

// $(document).ready(function(){
// 	$.ajax({
// 		url: window.location,
// 		type: 'POST',
// 		success: function(response){
// 			document.getElementById('paste_link').contentEditable = true;
// 			document.getElementById('paste_data').contentEditable = true;			
// 			$('#paste_link').attr("href","/" + response.paste_link);
// 			$('#paste_data').html(response.paste_text);
// 		},
// 		error: function(response){
// 			console.log(response);
// 		},
// 	});
// });
