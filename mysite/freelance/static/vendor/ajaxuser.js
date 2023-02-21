$(function() {
	// body...
	$('#search1').keyup(function() {
		// body...
		$.ajax({
			type: "POST",
			url: "/site/usearch/",
			data: {
				search_text : $('#search1').val(),
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
