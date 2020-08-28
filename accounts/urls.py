from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/edit/username', views.profile_edit_username, name='profile_edit_username'),
    path('profile/edit/bio', views.profile_edit_bio, name='profile_edit_bio'),
    path('me' , views.profile_me, name='profile_me'),
    path('<str:username>/', views.profile, name='profile'),
    path('welcome', views.welcome, name='welcome'),
    path('<str:username>/followers', views.followers, name='followers'),
    path('<str:username>/following', views.following, name='following'),
]

