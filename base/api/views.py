"""
Author: Francois Oratile Kgatlhanye
Date: 2026-06-04
Description: API for Oradio website.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Post
from .serializers import PostSerializer
from base.api import serializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/posts',
        'GET /api/posts/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getPosts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getPost(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)
