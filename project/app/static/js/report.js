$(document).delegate("#report_button","click",function(e){
	// alert('check')
	e.preventDefault();
	report_paste($('#paste_code').val());
});

var report_paste = function(text)
{
	var current_url = window.location.href;
	$.ajax({
		url: current_url,
		type: "POST",
		data:{'reason': text},
		success: function(response){
			window.location.assign(current_url.substring(0,current_url.length-11));
		},
		error: function(response){
			console.log(response);
			alert(response.responseJSON.error);
		},
	});
};
