from django.shortcuts import render, redirect
from models_core.models import UserProfile, Post, Comment
from django.contrib.auth.models import User

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

        # create a context, and render a template
        context = {
            'user': user,
            'user_profile': user_profile,
            'title': 'home',
            'following_list': following_list,
            'user_object' : User,
            'user_profile_object': UserProfile,
            'posts': posts
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
    comments = Comment.objects.filter(relation_upid=post.upid)

    if request.method == 'POST' : # if the user taps on the post button

        if request.POST['add-comment-input'] == '': # but if the field is empty, 

            # we return an error and redirect to the same path
            messages.error(request, 'you have to enter something in the comment field') 
            return redirect(request.path)

        # we get the input
        add_comment_input = request.POST['add-comment-input']

        # we create and save the comment
        comment = Comment(relation_email=user.email, relation_upid=post.upid, relation_user=user, relation_user_profile=user_profile, relation_post=post, content=add_comment_input)
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
            'comments': comments
        }

        return render(request, 'feed/post.html', context)

