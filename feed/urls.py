from django.urls import path
from . import views

urlpatterns = [
    path('add', views.add_post, name='add'),
    path('home', views.home, name='home'),
    path('<str:username>/<str:pid>/', views.post, name='post'),
    path('', views.redirect_home),
    path('ajax/get_has_liked', views.get_has_liked),
    path('ajax/post_like', views.post_like),
    path('ajax/post_unlike', views.post_unlike),
    path('ajax/get_comment_has_liked', views.get_comment_has_liked),
    path('ajax/post_comment_like', views.post_comment_like),
    path('ajax/post_comment_unlike', views.post_comment_unlike),
]
