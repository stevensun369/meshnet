from django.db import models
from datetime import datetime

from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    relation_email = models.TextField()

    profile_photo_url = models.TextField(default='/media/profile/profile.png')

    bio = models.TextField(blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)

    followers_list = models.TextField(blank=True)
    followers_count = models.IntegerField(default=0)

    following_list = models.TextField(blank=True)
    following_count = models.IntegerField(default=0)

    posts_liked = models.TextField(blank=True)
    posts_saved = models.TextField(blank=True)

    posts_count = models.IntegerField(default=0)

    def __str__(self):
        return self.relation_email


class Post(models.Model):
    relation_email = models.TextField()

    date_posted = models.DateTimeField(auto_now_add=True)

    relation_user = models.ForeignKey(User, on_delete=models.CASCADE)
    relation_user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    pid = models.TextField()
    upid = models.TextField()

    content = models.TextField()

    comments_count = models.IntegerField(default=0)

    likes_list = models.TextField(blank=True) 
    likes_count = models.IntegerField(default=0)

    def __str__(self):
        return self.upid


class Comment(models.Model):
    relation_email = models.TextField()
    relation_upid = models.TextField()
    date_commented = models.DateTimeField(auto_now_add=True)

    relation_user = models.ForeignKey(User, on_delete=models.CASCADE)
    relation_user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    relation_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    content = models.TextField()

    likes_list = models.TextField(blank=True)
    likes_count = models.IntegerField(default=0)

    def __str__(self):
        return self.relation_email





