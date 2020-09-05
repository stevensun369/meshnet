function changeLike(upid, user_email) {
    var upid = upid
    var user_email = user_email

    img_src_not_liked = '/static/img/heart-outline-blue.png'
    img_src_liked = '/static/img/heart-full-blue.png'

    // image select
    img = document.getElementById('img-' + upid)

    // number select
    number = document.getElementById('number-' + upid)



    var has_liked;
    var number_likes = parseInt(number.innerHTML, 10)

    // get if has liked or not
    $.ajax({
        'type': 'GET',
        'async': false,
        'url':'/ajax/get_has_liked',
        'data': {
            'upid': upid,
            'user_email': user_email,
        },
        'dataType': 'json', 
        'success': function (data) {
            document.getElementById('button-' + upid).value = data.has_liked
        },
    });

    has_liked = document.getElementById('button-' + upid).value
    // like or unlike
    if (has_liked == 'false') {
        $.ajax({
            'type': 'GET',
            'url': '/ajax/post_like',
            'data': {
                'upid': upid,
                'user_email': user_email,
            },
            'dataType': 'json',
            'success': function (data) {
            }
        })
        number_likes++
        img.src = img_src_liked
    } else if (has_liked == 'true') {
        $.ajax({
            'type': 'GET',
            'url': '/ajax/post_unlike',
            'data': {
                'upid': upid,
                'user_email': user_email,
            },
            'dataType': 'json',
            'success': function (data) {
            }
        })
        number_likes--
        img.src = img_src_not_liked
    }


    number.innerHTML = number_likes
}

function changeLikeComment(ucid, user_email) {

    img_src_not_liked = '/static/img/heart-outline-blue.png'
    img_src_liked = '/static/img/heart-full-blue.png'

    // image select
    img = document.getElementById('img-' + ucid)

    // number select
    number = document.getElementById('number-' + ucid)

    number_likes = parseInt(number.innerHTML, 10)



    var has_liked;

    // get if has liked or not
    $.ajax({
        'type': 'GET',
        'async': false,
        'url':'/ajax/get_comment_has_liked',
        'data': {
            'ucid': ucid,
            'user_email': user_email,
        },
        'dataType': 'json', 
        'success': function (data) {
            document.getElementById('button-' + ucid).value = data.has_liked
        },
    });

    has_liked = document.getElementById('button-' + ucid).value
    
    // like or unlike
    if (has_liked == 'false') {
        $.ajax({
            'type': 'GET',
            'url': '/ajax/post_comment_like',
            'data': {
                'ucid': ucid,
                'user_email': user_email,
            },
            'dataType': 'json',
            'success': function (data) {
                // alert(data.has_completed)
            }
        })
        number_likes++
        img.src = img_src_liked
    } else if (has_liked == 'true') {
        $.ajax({
            'type': 'GET',
            'url': '/ajax/post_comment_unlike',
            'data': {
                'ucid': ucid,
                'user_email': user_email,
            },
            'dataType': 'json',
            'success': function (data) {
                // alert(data.has_completed)
            }
        })
        number_likes--
        img.src = img_src_not_liked
    }


    number.innerHTML = number_likes
}
