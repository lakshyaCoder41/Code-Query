$(document).ready(function(){

  $('#vote').click(function(event){

    var v = $(this);
    var action = v.data('action');
    var commentID = v.data('commentid');
        $.ajax({
                 type: "POST",
                 url: "{% url 'vote-comment' %}",
                 data: { 'csrfmiddlewaretoken': '{{ csrf_token }}',commentID: commentID,
                        action: action},
                 dataType: "json",
                 success: function(response) {
                        alert(response.message);
                        alert('Upvotes' + response.likes_count);
                  },
                  error: function(rs, e) {
                         alert(rs.responseText);
                  }
            });
      })
});
