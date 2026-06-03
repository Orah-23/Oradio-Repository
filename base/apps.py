"""
Author: Francois Oratile Kgatlhanye
Date: 2026-06-04
Description: App configuration for Oradio website.
"""

from django.apps import AppConfig


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
