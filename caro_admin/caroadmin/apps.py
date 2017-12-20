from django.apps import AppConfig


class CaroadminConfig(AppConfig):
    name = 'caroadmin'

    # 重写父类ready方法
    def ready(self):
        super(CaroadminConfig, self).ready()

        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('caro')
