from django.apps import AppConfig


class QAConfig(AppConfig):
    name = 'qa'

    def ready(self):
        import qa.signals
