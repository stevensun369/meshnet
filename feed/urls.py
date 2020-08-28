from django.urls import path
from . import views

urlpatterns = [
    path('add', views.add_post, name='add'),
    path('home', views.home, name='home'),
    path('<str:username>/<str:pid>/', views.post, name='post'),
    path('', views.redirect_home)
]
