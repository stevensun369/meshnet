from django.shortcuts import render, redirect
from models_core.models import UserProfile, Post, Comment
from django.contrib.auth.models import User

from datetime import date

def home(request):

    if request.user.is_authenticated:

        user = User.objects.get(username=request.user)
        user_profile = UserProfile.objects.get(relation_email=user.email)

        following_list = user_profile.following_list.split(',')[:-1]
        following_list.append(user.email)

        posts = Post.objects.filter(relation_email__in=following_list).order_by('-date_posted')
        
        following_users = User.objects.filter(email__in=following_list)



        context = {
            'user': user,
            'user_profile': user_profile,
            'title': 'home',
            'following_list': following_list,
            'following_users': following_users,
            'user_object' : User,
            'user_profile_object': UserProfile,
            'posts': posts
        }
    
        return render(request, 'feed/home.html', context)
    else: 
        return redirect('welcome')


def redirect_home(request):
    return redirect('home')  


def add_post(request):
    user = User.objects.get(username=request.user)
    user_profile = UserProfile.objects.get(relation_email=user.email)

    today = date.today()
    pid_date = today.strftime('%Y') + today.strftime('%m') + today.strftime('%d')

    if request.method == 'POST':
        add_post_input = request.POST['add-post-input']

        id_counter = 0
        id_condition = False

        while not id_condition:
            if Post.objects.filter(relation_email=user.email, pid=pid_date + str(id_counter)).exists():
                id_counter += 1
            else: 
                id_condition = True

        post = Post(pid=pid_date+str(id_counter), relation_email=user.email, relation_user=user, relation_user_profile=user_profile, upid=user.email+'_'+pid_date+str(id_counter), content=add_post_input)
        user_profile.posts_count += 1
        post.save()
        user_profile.save()

        return redirect('home')

    else:
        context = {
            'user': user,
            'user_profile': user_profile,
        }
        
        return render(request, 'feed/add.html', context)

def post(request, username, pid):
    user = User.objects.get(username=request.user)
    user_profile = UserProfile.objects.get(relation_email=user.email)

    target = User.objects.get(username=username)
    target_profile = UserProfile.objects.get(relation_email = target.email)

    post = Post.objects.get(upid=target.email+'_'+pid)
    comments = Comment.objects.filter(relation_upid=post.upid)

    if request.method == 'POST':

        add_comment_input = request.POST['add-comment-input']

        comment = Comment(relation_email=user.email, relation_upid=post.upid, relation_user=user, relation_user_profile=user_profile, relation_post=post, content=add_comment_input)
        post.comments_count += 1
        comment.save()
        post.save()

        return redirect('/'+target.username+'/'+post.pid+'/')

    else:

        context = {
            'user':user,
            'user_profile': user_profile,
            'target': target,
            'target_profile': target_profile,
            'post':post,
            'comments': comments
        }

        return render(request, 'feed/post.html', context)

