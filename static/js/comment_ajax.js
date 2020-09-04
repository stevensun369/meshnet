function add_comment(user_email, post_upid) {
    var comments_container = document.getElementById('comments-container').innerHTML
    var comment_content = document.getElementById('comment-content').value

    comment_condition = true
    
    if (!comment_content.trim()) {
        alert('The comment field cannot be empty or contain only spaces.')
        var comment_condition = false
    }

    if (comment_condition) {
        $.ajax({
            'type': 'GET',
            'url': '/ajax/post_add_comment',
            'data': {
                'user_email': user_email,
                'post_upid': post_upid,
                'comment_content': comment_content
            },
            'dataType': 'json',
            'success': function (data) {
                // extremely dumb way, but i have no other way without using any type of framework
                new_comment = 
                '<div class="comment">' + 
                    '<a href="/' + data.user_username + '">'+
                        '<img src="' + data.user_photo + '" class="comment-profile-img">' + 
                    '</a>' +

                    '<a href="/' + data.user_username + '">'+
                        '<div class="comment-info">' +
                            '<div class="comment-info-row user-handle">' +
                                '@' + data.user_username +
                            '</div>' +
                            '<div class="comment-info-row comment-date">' +
                                'now'+
                            '</div>'+
                        '</div>'+
                    '</a>' +

                    '<div class="comment-content">' +
                        data.comment_content +
                    '</div>' +

                    '<div class="comment-actions">' + 
                        '<div class="comment-actions-action">' + 
                            '<button onclick="changeLikeComment(\'' + data.comment_ucid + '\', \'' + data.user_email + '\')" class="comment-actions-action-img-button" value="" id="button-' + data.comment_ucid + '">' +
                                '<img src="/static/img/heart-outline-blue.png" class="comment-actions-action-img" id="img-' + data.comment_ucid + '">' + 
                            '</button>' + 
                            '<span class="comment-actions-action-number" id="number-' + data.comment_ucid + '">' + data.comment_likes_count + '</span>' +
                        '</div>' + 
                    '</div>' + 
                '</div>' ;


                document.getElementById('comments-container').innerHTML = new_comment + comments_container
                document.getElementById('comment-content').value = ''
            }
        })


    }
}