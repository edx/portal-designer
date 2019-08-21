""" app config for designer core """

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'designer.apps.core'

    def ready(self):
        from . import signals  # pylint: disable=unused-variable
