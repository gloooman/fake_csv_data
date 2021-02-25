from django.apps import AppConfig


class CreatorConfig(AppConfig):
    name = 'creator'

    def ready(self):
        try:
            import creator.signals
        except ImportError:
            pass
