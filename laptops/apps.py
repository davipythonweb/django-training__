# from django.apps import AppConfig


# class LaptopsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'laptops'
    
    
#     def ready(self):
#         import laptops.signals

from django.apps import AppConfig

class LaptopsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'laptops'

    def ready(self):
        from .signals import register_signals
        register_signals()