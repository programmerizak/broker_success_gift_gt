from django.apps import AppConfig


class CopyTraderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'copy_trader'

    def ready(self):
        import copy_trader.signals
