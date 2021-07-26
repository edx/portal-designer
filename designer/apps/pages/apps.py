"""
App Configuration for pages
"""
from django.apps import AppConfig


class PagesConfig(AppConfig):
    """
    Django AppConfig class for the pages application.
    """
    name = 'pages'

    # In Django 3.2, app configuration is automatically selected from apps.py
    # submodule in case of single config class in apps.py module, to disable
    # this feature we need to set `default = False` in AppConfig of that app
    # https://docs.djangoproject.com/en/3.2/ref/applications/#configuring-applications
    default = False
