from django.apps import AppConfig

class CarlogoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carLogo'

    def ready(self):
        from .utils import model_loader
        from . import views

        views.model, views.device, views.label_dict = model_loader.load_model()
