from django.apps import AppConfig

class FixithubappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fixithubapp'

    def ready(self):
        import fixithubapp.signals
