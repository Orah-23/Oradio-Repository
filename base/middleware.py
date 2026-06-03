"""
Author: Francois Oratile Kgatlhanye
Date: 2026-06-04
Description: Middleware for Oradio website.
"""

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class LastSeenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            request.user.__class__.objects.filter(pk=request.user.pk).update(
                last_seen=timezone.now()
            )