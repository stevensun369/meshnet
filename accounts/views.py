from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.files.storage import FileSystemStorage

from models_core.models import UserProfile, Post

from django.http import HttpResponseRedirect, HttpResponse


def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        password_condition = False
        email_condition = False
        username_condition = False

        # password condition
        if password != password_confirm:
            messages.error(request, 'passwords do not match')
        else:
            password_condition = True


        # email condition
        if User.objects.filter(email=email).exists():
            messages.error(request, 'email already in use')
        else: 
            email_condition = True

        #username condition
        if User.objects.filter(username=username).exists():
            messages.error(request, 'username already exists')
        else:
            username_condition = True

        if password_condition and email_condition and username_condition:
            # we will create a user
            user = User.objects.create_user(username=username, email=email, password=password,
            )
            user.save()

            user_profile = UserProfile(relation_email=email)
            user_profile.save()

            messages.success(request, 'you are now registered, and can log in')
            return redirect('login')
        else: 
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you have been successfully logged in')
            return redirect('home')
        else:
            messages.error(request, 'invalid credentials')
            return redirect('login')

    else:
        return render(request, 'accounts/login.html')


def profile(request, username):

    user = User.objects.get(username=request.user)
    user_profile = UserProfile.objects.get(relation_email=user.email)

    target = User.objects.get(username=username)
    target_profile = UserProfile.objects.get(relation_email=target.email)

    target_followers_list = target_profile.followers_list.split(',')
    user_following_list = user_profile.following_list.split(',')

    if user.email in target_followers_list and target.email in user_following_list:
        follow_condition = True
    else:
        follow_condition = False

    if request.method == 'POST':
        submit_button = request.POST['input']

        if submit_button == 'follow':
            target_profile.followers_list += user.email + ','
            target_profile.followers_count += 1

            user_profile.following_list += target.email + ','
            user_profile.following_count = user_profile.following_count + 1

            target_profile.save()
            user_profile.save()

        elif submit_button == 'unfollow':
            target_followers_list.remove(user.email)
            target_profile.followers_list = ','.join(target_followers_list)
            target_profile.followers_count -= 1

            user_following_list.remove(target.email)
            user_profile.following_list = ','.join(user_following_list)
            user_profile.following_count -= 1 

            target_profile.save()
            user_profile.save()

        return redirect('/' + username)

    else:

        posts = Post.objects.filter(relation_email=target.email).order_by('-date_posted')

        context = {
            'target': target,
            'target_profile': target_profile,
            'user': user,
            'user_profile': user_profile,
            'target_followers_list' : target_followers_list,
            'user_following_list': user_following_list,
            'follow_condition': follow_condition,
            'posts': posts
        }

        return render(request, 'accounts/profile.html', context)

def profile_me(request):
    user = User.objects.get(username=request.user)
    user_profile = UserProfile.objects.get(relation_email=user.email)

    posts = Post.objects.filter(relation_email=user.email).order_by('-date_posted')


    context = {
        'user': user,
        'user_profile': user_profile,
        'posts': posts
    }

    return render(request, 'accounts/me.html', context)
def profile_edit(request):

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        user_profile = UserProfile.objects.get(relation_email=user.email)

        context = {
            'user': user,
            'user_profile': user_profile 
        }

        return render(request, 'accounts/profile_edit.html', context)
            
    else:
        return redirect('register')

def profile_edit_username(request):

    if request.method == 'POST':
        edit_username_input = request.POST['edit-username-input']

        if User.objects.filter(username=edit_username_input).exists():
            username_condition = False
            messages.error(request, 'username already exists, choose another one')
        else:
            username_condition = True

        if not username_condition:
            return redirect(request.path)
        else:
            user = User.objects.get(username=request.user)
            user.username = edit_username_input
            user.save()
            success_message = 'you have successfuly updated your username'
            messages.success(request, success_message)
            return redirect('profile_edit')

    else: 
        return render(request, 'accounts/profile_edit_username.html')

def profile_edit_bio(request):
    
    if request.method == 'POST':
        edit_bio_input = request.POST['edit-bio-input']

        user = User.objects.get(username=request.user)
        user_profile = UserProfile.objects.get(relation_email=user.email)

        user_profile.bio = edit_bio_input
        user_profile.save()

        messages.success(request, 'you have successfuly updated your bio')
        # return redirect('profile_edit')

        return redirect('/profile/edit')

    else: 

        user = User.objects.get(username=request.user)
        user_profile = UserProfile.objects.get(relation_email=user.email)

        context = {
            'user': user,
            'user_profile': user_profile,
        }
        return render(request, 'accounts/profile_edit_bio.html', context)

def profile_edit_photo(request):
    user = User.objects.get(username=request.user)
    user_profile = UserProfile.objects.get(relation_email=user.email)

    if request.method == "POST" and request.FILES['profile_photo']:
        profile_photo = request.FILES['profile_photo']

        fs = FileSystemStorage()

        filename = fs.save(profile_photo.name, profile_photo)

        uploaded_file_url = fs.url(filename)

        user_profile.profile_photo_url = uploaded_file_url
        user_profile.save()

        messages.success(request, 'you have successfuly changed your profile photo')

        return redirect('/profile/edit')

    context = {
        'user': user,
        'user_profile': user_profile,
    }

    return render(request, 'accounts/profile_edit_photo.html', context)

def welcome(request):
    return render(request, 'accounts/welcome.html')


def followers(request, username):
    # getting the target user 
    target = User.objects.get(username=username)
    target_profile = UserProfile.objects.get(relation_email=target.email)

    # seriliazing the followers field into a list
    target_followers = target_profile.followers_list.split(',')[0:-1]

    #creating the  user queryset
    followers = User.objects.filter(email__in=target_followers)
    followers_profile = UserProfile.objects.filter(relation_email__in=target_followers)
  

    context  = {
        'target': target,
        'target_followers':target_followers,
        'followers': followers,
        'followers_profile': followers_profile,
        'zipped_followers': zip(followers, followers_profile),
    }

    return render(request, 'accounts/followers.html', context)

def following(request, username):
    # getting the target user
    target = User.objects.get(username=username)
    target_profile = UserProfile.objects.get(relation_email=target.email)

    # seriliazing the following field into a list
    target_following = target_profile.following_list.split(',')[0:-1]

    #creating the  user queryset
    following = User.objects.filter(email__in=target_following)
    following_profile = UserProfile.objects.filter(relation_email__in=target_following)
  

    context  = {
        'target': target,
        'target_following':target_following,
        'following': following,
        'following_profile': following_profile,
        'zipped_following': zip(following, following_profile),
    }

    return render(request, 'accounts/following.html', context)

