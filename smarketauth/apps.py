from django.apps import AppConfig


class SmarketauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smarketauth'

    def ready(self):
        import smarketauth.signals
