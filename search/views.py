from django.shortcuts import render
from models_core.models import User, UserProfile

def search(request):

    users = User.objects.order_by('-date_joined')
    users_profile = UserProfile.objects.filter(id=-1)

    if 'q' in request.GET:
        q = request.GET['q']
        if q:
            users = users.filter(username__icontains=q)
            for user in users:
                user_profile = UserProfile.objects.filter(relation_email=user.email)
                users_profile = users_profile | user_profile

    context = {
        'users': users,
        'users_profile': users_profile.order_by('-date_joined'),
        'zipped_users': zip(users, users_profile.order_by('-date_joined')),
        'get_values': request.GET,
    }

    return render(request, 'search/search.html', context)