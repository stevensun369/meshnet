function changeFollow(user_email, target_email) {
    var has_followed;

    var button = document.getElementById('follow-button')
    var followers_number = document.getElementById('followers-number')

    button_follow_className = 'profile-follow-button'
    button_unfollow_className = 'profile-unfollow-button'

    $.ajax({
        'type': 'GET',
        'async': false,
        'url': '/ajax/get_has_followed',
        'data': {
            'user_email': user_email,
            'target_email': target_email,
        },
        'dataType': 'json',
        'success': function (data) {
            button.value = data.has_followed
        }
    })

    has_followed = button.value

    if (has_followed == 'false') {
        
        $.ajax({
            'type': 'GET',
            'url': '/ajax/post_follow',
            'data': {
                'user_email': user_email,
                'target_email': target_email,
            },
            'dataType': 'json',
            'success': function (data) {
                // alert(data.has_completed)
            }
        })

        followers_number.innerHTML = parseInt(followers_number.innerHTML, 10) + 1
        button.className = button_unfollow_className
        button.innerHTML = 'unfollow'

    } else if (has_followed == 'true') {
        $.ajax({
            'type': 'GET',
            'url': '/ajax/post_unfollow',
            'data': {
                'user_email': user_email,
                'target_email': target_email,
            },
            'dataType': 'json',
            'success': function (data) {
                // alert(data.has_completed)
            }
        })

        followers_number.innerHTML = parseInt(followers_number.innerHTML, 10) - 1
        button.className = button_follow_className
        button.innerHTML = 'follow'
    }


    


}