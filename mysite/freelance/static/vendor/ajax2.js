$(function() {
	// body...
	$('#search2').keyup(function() {
		// body...
		$.ajax({
			type: "POST",
			url: "/site/w/csearch/",
			data: {
				search_text : $('#search2').val(),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: searchSuccess,
			dataType:'html'
		});

	});
});

function searchSuccess(data,textStatus,jqXHR) 
{
	$('#search-results').html(data);
}
