"""
Author: Francois Oratile Kgatlhanye
Date: 2026-06-04
Description: Serializer for Oradio website.
"""

from rest_framework.serializers import ModelSerializer
from base.models import Post


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
