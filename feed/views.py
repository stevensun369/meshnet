from django.shortcuts import render, redirect
from models_core.models import UserProfile, Post, Comment
from django.contrib.auth.models import User
from django.http import JsonResponse

from django.contrib import messages

from datetime import date

def home(request):

    if request.user.is_authenticated: # first we check if a user is authenticated

        # we get the user data
        user = User.objects.get(username=request.user)
        user_profile = UserProfile.objects.get(relation_email=user.email)

        # and serialize the following list, also adding his own email to it.
        following_list = user_profile.following_list.split(',')[:-1]
        following_list.append(user.email)

        # we create a post variable, that will hold all of the posts
        posts = Post.objects.filter(relation_email__in=following_list).order_by('-date_posted')

        liked_list = []

        for post in posts: # we iterate through posts
            if user.email in post.likes_list: # and if the user liked the post, we append true to the list
                liked_list.append('true')
            elif user.email not in post.likes_list: # but if the user didn't like the post, we append false to the list
                liked_list.append('false')

        # create a context, and render a template
        context = {
            'user': user,
            'user_profile': user_profile,
            'title': 'home',
            'following_list': following_list,
            'user_object' : User,
            'user_profile_object': UserProfile,
            'posts': posts,
            'liked_list': liked_list,
            'zipped': zip(liked_list, posts)
        }
    
        return render(request, 'feed/home.html', context)

    else: # and if not, we get him/she to the welcome page
        return redirect('welcome')


def redirect_home(request):

    # redirects home
    return redirect('home')  


def add_post(request):

    # we get the user info, and some other helpful variables
    user = User.objects.get(username=request.user)
    user_profile = UserProfile.objects.get(relation_email=user.email)

    today = date.today()
    pid_date = today.strftime('%Y') + today.strftime('%m') + today.strftime('%d')

    if request.method == 'POST': # if user taps post

        if request.POST['add-post-input'] == '':

            # we give an error message, and redirect to the same path
            messages.error(request, 'you have to enter something in the post field')
            return redirect(request.path)

        # we get the input
        add_post_input = request.POST['add-post-input']

        id_counter = 0
        id_condition = False

        while not id_condition: # we get the id_counter for the post pid and upid
            if Post.objects.filter(relation_email=user.email, pid=pid_date + str(id_counter)).exists():
                id_counter += 1
            else: 
                id_condition = True

        # create a post, and save
        post = Post(pid=pid_date+str(id_counter), relation_email=user.email, relation_user=user, relation_user_profile=user_profile, upid=user.email+'_'+pid_date+str(id_counter), content=add_post_input)
        post.save()

        # also increment posts_count, and save the user_profile
        user_profile.posts_count += 1
        user_profile.save()

        return redirect('home')

    else: # if not clicked on post, 

        # we create context, and render a template
        context = {
            'user': user,
            'user_profile': user_profile,
        }
        
        return render(request, 'feed/add.html', context)

def post(request, username, pid):

    # we get the user and target
    user = User.objects.get(username=request.user)
    user_profile = UserProfile.objects.get(relation_email=user.email)

    target = User.objects.get(username=username)
    target_profile = UserProfile.objects.get(relation_email = target.email)

    # get the post and the comment
    post = Post.objects.get(upid=target.email+'_'+pid)
    comments = Comment.objects.filter(relation_upid=post.upid).order_by('-date_commented')

    liked = user.email in post.likes_list

    comment_liked = []
    for comment in comments:
        if user.email in comment.likes_list:
            comment_liked.append('true')
        elif user.email not in comment.likes_list:
            comment_liked.append('false')

    today = date.today()
    cid_date = today.strftime('%Y') + today.strftime('%m') + today.strftime('%d')

    if request.method == 'POST' : # if the user taps on the post button

        if request.POST['add-comment-input'] == '': # and the field is empty, 

            # we return an error and redirect to the same path
            messages.error(request, 'you have to enter something in the comment field') 
            return redirect(request.path)

        # we get the input
        add_comment_input = request.POST['add-comment-input']

        id_counter = 0
        id_condition = False

        while not id_condition: # we get the id_counter for the post pid and upid
            if Comment.objects.filter(ucid=post.upid+'_'+user.email+'_'+cid_date+str(id_counter)).exists():
                id_counter += 1
            else: 
                id_condition = True
                ucid = post.upid+'_'+user.email+'_'+cid_date+str(id_counter)
        
        # we create and save the comment
        comment = Comment(relation_email=user.email, relation_upid=post.upid, ucid=ucid, relation_user=user, relation_user_profile=user_profile, relation_post=post, content=add_comment_input)
        comment.save()

        # we increase the comments counter
        post.comments_count += 1
        post.save()

        return redirect(request.path)

    else:

        # if the user doesn't tap the send button, we just render a template
        context = {
            'user':user,
            'user_profile': user_profile,
            'target': target,
            'target_profile': target_profile,
            'post':post,
            'comments': comments,
            'liked': liked,
            'comment_liked': comment_liked,
            'zipped_comments': zip(comment_liked, comments)
        }

        return render(request, 'feed/post.html', context)


def get_has_liked(request):

    upid = request.GET.get('upid', None)
    user_email = request.GET.get('user_email', None)

    post = Post.objects.get(upid=upid)

    has_liked = user_email in post.likes_list

    data = {
        'has_liked': has_liked,
    }

    return JsonResponse(data)


def post_like(request):

    upid = request.GET.get('upid', None)
    user_email = request.GET.get('user_email', None)

    post = Post.objects.get(upid=upid)

    post.likes_list += user_email + ','
    post.likes_count += 1
    post.save()

    data = {
        'has_completed': 'liked'
    }

    return JsonResponse(data)

def post_unlike(request):

    upid = request.GET.get('upid', None)
    user_email = request.GET.get('user_email', None)

    post = Post.objects.get(upid=upid)

    post_likes_list = post.likes_list.split(',')

    post_likes_list.remove(user_email)
    post.likes_list = ','.join(post_likes_list)
    post.likes_count -= 1

    post.save()

    data = {
        'has_completed': 'unliked'
    }

    return JsonResponse(data)

def get_comment_has_liked(request):

    ucid = request.GET.get('ucid', None)
    user_email = request.GET.get('user_email', None)

    comment = Comment.objects.get(ucid=ucid)

    has_liked = user_email in comment.likes_list

    data = {
        'has_liked': has_liked
    }

    return JsonResponse(data)


def post_comment_like(request):

    ucid = request.GET.get('ucid', None)
    user_email = request.GET.get('user_email', None)

    comment = Comment.objects.get(ucid=ucid)

    comment.likes_list += user_email + ','
    comment.likes_count += 1
    comment.save()

    data = {
        'has_completed': 'like'
    }

    return JsonResponse(data)

def post_comment_unlike(request):

    ucid = request.GET.get('ucid', None)
    user_email = request.GET.get('user_email', None)

    comment = Comment.objects.get(ucid=ucid)

    comment_likes_list = comment.likes_list.split(',')

    comment_likes_list.remove(user_email)
    comment.likes_list = ','.join(comment_likes_list)
    comment.likes_count -= 1

    comment.save()

    data = {
        'has_completed': 'unlike'
    }

    return JsonResponse(data)

    
def post_add_comment(request):
    
    user_email = request.GET.get('user_email', None)
    post_upid = request.GET.get('post_upid', None)
    comment_content = request.GET.get('comment_content', None)

    user = User.objects.get(email=user_email)
    user_profile = UserProfile.objects.get(relation_email=user_email)

    post = Post.objects.get(upid=post_upid)

    # we get the ucid
    today = date.today()
    cid_date = today.strftime('%Y') + today.strftime('%m') + today.strftime('%d')

    id_counter = 0
    id_condition = False

    while not id_condition: # we get the id_counter for the post pid and upid
        if Comment.objects.filter(ucid=post.upid+'_'+user.email+'_'+cid_date+str(id_counter)).exists():
            id_counter += 1
        else: 
            id_condition = True
            ucid = post.upid+'_'+user.email+'_'+cid_date+str(id_counter)
    
    # we create and save the comment
    comment = Comment(relation_email=user.email, relation_upid=post.upid, ucid=ucid, relation_user=user, relation_user_profile=user_profile, relation_post=post, content=comment_content)
    comment.save()

    # we increase the comments counter
    post.comments_count += 1
    post.save()

    comment = Comment.objects.get(ucid=ucid)

    data = {
        'has_completed': 'comment has been sent',
        'user_username': user.username,
        'user_email': user.email,
        'user_photo': user_profile.profile_photo_url,
        'comment_content': comment.content,
        'comment_ucid': comment.ucid,
        'comment_likes_count': comment.likes_count,
    }

    return JsonResponse(data)




    
