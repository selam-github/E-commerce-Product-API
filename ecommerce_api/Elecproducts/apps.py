from django.apps import AppConfig


class ElecproductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Elecproducts'

def ready(self):
        import Elecproducts.signals  # Ensure that signals are registered when the app is ready