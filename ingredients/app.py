from django.apps import AppConfig
from django.db.models.signals import post_delete


class IngredientsAppConfig(AppConfig):
    name = "ingredients"

    def ready(self):
        print("ProductAppConfig111")
