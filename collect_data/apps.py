from django.apps import AppConfig


class CollectDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collect_data'

    def ready(self):
        from track_price import automate
        automate.start()
