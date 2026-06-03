"""
Author: Francois Oratile Kgatlhanye
Date: 2026-06-04
Description: API URLs for Oradio website.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('',  views.getRoutes),
    path('posts/', views.getPosts),
    path('posts/<str:pk>/', views.getPost),
]
