from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.files.storage import FileSystemStorage

from models_core.models import UserProfile, Post

from django.http import HttpResponseRedirect, HttpResponse


def register(request):

    if request.method == 'POST': # if submit button is pressed

        # we get the respective inputs
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        # we instantiate the condition, so now exception is going to be thrown when I assing it
        password_condition = False
        email_condition = False
        username_condition = False

        # password condition verification
        if password != password_confirm:
            messages.error(request, 'passwords do not match')
        else:
            password_condition = True


        # email condition verification
        if User.objects.filter(email=email).exists():
            messages.error(request, 'email already in use')
        else: 
            email_condition = True

        #username condition verification
        if User.objects.filter(username=username).exists():
            messages.error(request, 'username already exists')
        else:
            username_condition = True

        if password_condition and email_condition and username_condition: # if all the conditions are met

            # we will create a user
            user = User.objects.create_user(username=username, email=email, password=password,) # we create a User and save it
            user.save()

            user_profile = UserProfile(relation_email=email) # and we also create a UserProfile and save it
            user_profile.save()

            messages.success(request, 'you are now registered, and can log in')
            return redirect('login') # we go to login

        else: 
            return redirect('register') # if the conditions are not met, we redirect to the register page to try again.
    else:
        return render(request, 'accounts/register.html') # yet, if the method is not post, meaning I just load the page, it simply renders and html page


def login(request):

    # note: this is very similar to register(), just that we check the user, not create it.

    if request.method == 'POST': 

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        
        if user is not None: # is a user is found using the credentials introduced, it authenticates
            auth.login(request, user)
            messages.success(request, 'you have been successfully logged in')
            return redirect('home')
        else: # but if not, we throw a message error 
            messages.error(request, 'invalid credentials')
            return redirect('login')

    else:
        return render(request, 'accounts/login.html')


def profile(request, username):

    # we get the user variables that we need (including the followers and following list for following somebody)
    user = User.objects.get(username=request.user)
    user_profile = UserProfile.objects.get(relation_email=user.email)

    target = User.objects.get(username=username)
    target_profile = UserProfile.objects.get(relation_email=target.email)

    target_followers_list = target_profile.followers_list.split(',')
    user_following_list = user_profile.following_list.split(',')

    # if the user is already following the target, we set the following_condition to true
    if user.email in target_followers_list and target.email in user_following_list:
        follow_condition = True
    else: # else we set it to false
        follow_condition = False

    if request.method == 'POST': # if the user presses the follow/unfollow button, we get the contents of the input(either 'follow' or 'unfollow')

        submit_button = request.POST['input']

        if submit_button == 'follow':

            target_profile.followers_list += user.email + ',' # we add the user to the target's followers list
            target_profile.followers_count += 1 # and increase the followers counter of the target by 1

            user_profile.following_list += target.email + ',' # now, we add the target to the user's following list.
            user_profile.following_count = user_profile.following_count + 1 # and increase the user's following counter by 1

            # and we save both profiles
            target_profile.save()
            user_profile.save()

        elif submit_button == 'unfollow':

            target_followers_list.remove(user.email) # we remove the user from the python target's followers list
            target_profile.followers_list = ','.join(target_followers_list) # we reassign the list to the TextField in the model
            target_profile.followers_count -= 1 # decrease count by 1

            user_following_list.remove(target.email) # we remove the target from the pytho nuser's following list
            user_profile.following_list = ','.join(user_following_list) # we reassign the list to the TextField in the model
            user_profile.following_count -= 1 # decrease count by 1

            # save both profiles
            target_profile.save()
            user_profile.save()

        return redirect('/' + username)

    else: # but if the user doesn't press the follow/unfollow button, we simply create a posts variable, create context, and render a template

        posts = Post.objects.filter(relation_email=target.email).order_by('-date_posted')

        liked_list = []

        for post in posts: # we iterate through posts
            if user.email in post.likes_list: # and if the user liked the post, we append true to the list
                liked_list.append('true')
            elif user.email not in post.likes_list: # but if the user didn't like the post, we append false to the list
                liked_list.append('false')


        context = {
            'target': target,
            'target_profile': target_profile,
            'user': user,
            'user_profile': user_profile,
            'target_followers_list' : target_followers_list,
            'user_following_list': user_following_list,
            'follow_condition': follow_condition,
            'posts': posts,
            'liked_list': liked_list,
            'zipped': zip(liked_list, posts)
        }

        return render(request, 'accounts/profile.html', context)

def profile_me(request):

    # we simply get the user variabels from the request.user object
    user = User.objects.get(username=request.user)
    user_profile = UserProfile.objects.get(relation_email=user.email)

    # get all of the users posts
    posts = Post.objects.filter(relation_email=user.email).order_by('-date_posted')

    liked_list = []

    for post in posts: # we iterate through posts
        if user.email in post.likes_list: # and if the user liked the post, we append true to the list
            liked_list.append('true')
        elif user.email not in post.likes_list: # but if the user didn't like the post, we append false to the list
            liked_list.append('false')

    # create context
    context = {
        'user': user,
        'user_profile': user_profile,
        'posts': posts,
        'liked_list': liked_list,
        'zipped' : zip(liked_list, posts)
    }

    # and render a template
    return render(request, 'accounts/me.html', context)

def profile_edit(request):

    if request.user.is_authenticated: # first we check if a user is_authenticated

        user = User.objects.get(username=request.user)
        user_profile = UserProfile.objects.get(relation_email=user.email)

        context = {
            'user': user,
            'user_profile': user_profile,
        }

        return render(request, 'accounts/profile_edit.html', context)
            
    else: # if not, we redirect to welcome
        return redirect('welcome')

def profile_edit_username(request):

    if request.method == 'POST': # if save is pressed

        edit_username_input = request.POST['edit-username-input'] # we get the input

        # we check if the username in the input already exists
        if User.objects.filter(username=edit_username_input).exists():
            username_condition = False
            messages.error(request, 'username already exists, choose another one')
        else:
            username_condition = True

        if not username_condition: # and if the username already exists, we redirect to the same path, with a django message
            return redirect(request.path)
        else: # but if the username doesn't exist
            user = User.objects.get(username=request.user) # we get the user
            user.username = edit_username_input # we modify it's username
            user.save() # we save it
            messages.success(request, 'you have successfuly updated your username' ) # we give a success message
            return redirect('profile_edit') # and redirect to profile edit

    else: # else, we just render the template
        return render(request, 'accounts/profile_edit_username.html')

def profile_edit_bio(request):
    
    # if the user click save
    if request.method == 'POST':

        edit_bio_input = request.POST['edit-bio-input'] # we get the input

        # we get the user 
        user = User.objects.get(username=request.user)
        user_profile = UserProfile.objects.get(relation_email=user.email)

        # modify the bio, and save
        user_profile.bio = edit_bio_input
        user_profile.save()

        messages.success(request, 'you have successfuly updated your bio')

        return redirect('/profile/edit')

    else: 

        # else, we just render a template with some user and user_profile context
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

    if request.method == "POST" and request.FILES['profile_photo']: # if the user presses save
        profile_photo = request.FILES['profile_photo'] # we get the photo

        # save the file to the FileSystemStorage, and get it's name
        fs = FileSystemStorage()
        filename = fs.save(profile_photo.name, profile_photo)
        uploaded_file_url = fs.url(filename)

        # modify the user profile photo, and save it
        user_profile.profile_photo_url = uploaded_file_url
        user_profile.save()

        messages.success(request, 'you have successfuly changed your profile photo')

        return redirect('/profile/edit')

    else: # else we just render a template

        user = User.objects.get(username=request.user)
        user_profile = UserProfile.objects.get(relation_email=user.email)

        context = {
            'user': user,
            'user_profile': user_profile,
        }

        return render(request, 'accounts/profile_edit_photo.html', context)

def welcome(request):

    # pretty much a static page
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

