from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('profile/edit/photo', views.profile_edit_photo, name='profile_edit_photo'),
    path('profile/edit/username', views.profile_edit_username, name='profile_edit_username'),
    path('profile/edit/bio', views.profile_edit_bio, name='profile_edit_bio'),
    path('profile' , views.profile_me, name='profile_me'),
    path('<username>/', views.profile, name='profile'),
    path('welcome', views.welcome, name='welcome'),
    path('<username>/followers', views.followers, name='followers'),
    path('<username>/following', views.following, name='following'),

    #ajax
    path('ajax/get_has_followed', views.get_has_followed),
    path('ajax/post_follow', views.post_follow),
    path('ajax/post_unfollow', views.post_unfollow)
]

