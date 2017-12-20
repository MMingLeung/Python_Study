from django.apps import AppConfig


class MattadminConfig(AppConfig):
    name = 'mattadmin'

    def ready(self):
        super(MattadminConfig, self).ready()

        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('madmin')
