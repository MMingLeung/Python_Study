from django.apps import AppConfig


class SupermattConfig(AppConfig):
    name = 'supermatt'

    def ready(self):
        '''
        程序刚运行时，执行该方法
        :return: 
        '''
        super(SupermattConfig, self).ready()

        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('smatt')