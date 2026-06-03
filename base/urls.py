"""
Author: Francois Oratile Kgatlhanye
Date: 2026-06-04
Description: URLs for Oradio website.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('', views.home, name="home"),
    path('post/<str:pk>/', views.post, name="post"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-post/', views.createPost, name="create-post"),
    path('update-post/<str:pk>/', views.updatePost, name="update-post"),
    path('delete-post/<str:pk>/', views.deletePost, name="delete-post"),
    
    path('reply-comment/<str:pk>/', views.replyComment, name="reply-comment"),
    path('delete-comment/<str:pk>/', views.deleteComment, name="delete-comment"),

    path('update-user/', views.updateUser, name="update-user"),
    
    path('follow-user/<str:pk>/', views.followUser, name="follow-user"),
    path('unfollow-user/<str:pk>/', views.unfollowUser, name="unfollow-user"),
    
    path('react/<str:pk>/', views.react, name="react"),
    path('unreact/<str:pk>/', views.unreact, name="unreact"),
    
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<str:pk>/', views.conversation, name='conversation'),
    path('new-conversation/<str:pk>/', views.newConversation, name='new-conversation'),
    
    path('reply-comment/<str:pk>/', views.replyComment, name="reply-comment"),
]
