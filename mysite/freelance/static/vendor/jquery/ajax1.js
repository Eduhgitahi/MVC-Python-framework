 $(function() {
  // body...
  $('#search').keyup(function() {
    // body...
    $.ajax({
      type: "POST",
      url: "/site/w/search/",
      data: {
        search_text1 : $('#search').val(),
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