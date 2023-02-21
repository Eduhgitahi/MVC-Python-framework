
$(function(){

	$(document).load(function(){
		$.ajax({
			type: "POST",
			url: "/site/notify/",
			data: {
				status: $(0).val(),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: Success,
			dataType:'html'
		});
	});
});

function Success(data,textStatus,jqXHR) 
{
	alert('Thank you!!')
}