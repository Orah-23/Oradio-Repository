"""
Author: Francois Oratile Kgatlhanye
Date: 2026-06-04
Description: Models for Oradio website.
"""

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )

    avatar = models.ImageField(upload_to='avatars/', null=True, default="avatar.svg")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    @property
    def is_online(self):
        if self.last_seen:
            return (timezone.now() - self.last_seen).seconds < 300  # 5 min window
        return False
    
    def total_followers(self):
        return self.followers.count()

    def total_following(self):
        return self.following.count()

    def __str__(self):
        return self.username


class Post(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    caption = models.TextField(null=True, blank=True)
    body = models.FileField(upload_to='posts/')
    users_reacted = models.ManyToManyField(
        User,
        related_name='reactors',
        blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.host.username + "-" + self.caption


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.FileField(upload_to='comments/')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ['-updated', '-created']
 
    def __str__(self):
        return self.user.username + "-" + str(self.created)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"{self.sender} → {self.recipient}: {self.body[:30]}"
