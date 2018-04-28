from django.apps import AppConfig


class CryptoAppConfig(AppConfig):
    name = 'crypto_app'

    def ready(self):
        import crypto_app.tasks
