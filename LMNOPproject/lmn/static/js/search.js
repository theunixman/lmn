//Trying to implement ajax auto complete search for notes at this url http://127.0.0.1:8000/notes/latest/
// I want to load the html data from http://127.0.0.1:8000/notes/search to this function  and provide a base on What
// the user is typing in the input box with id #search
$(function() {
  $('#search').keyup(function() {
    $.ajax({
      type: "POST",
      url: "/notes/search/",
      data: {
        'search_text' : $('#search').val(),
        'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
      },
      sucess : searchSucess,
      dataType: 'html'
    });
  });
});


function searchSucess(data, textStatus, jqXHR) {
  $('#search-results').html(data);

}
