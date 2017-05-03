from __future__ import unicode_literals

from django.apps import AppConfig


class DataSourcesConfig(AppConfig):
    name = 'data'

    def ready(self):
        pass
