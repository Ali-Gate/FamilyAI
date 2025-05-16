from django.apps import AppConfig

class FamilyAiAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'family_ai_app'

    def ready(self):
        # Import signals to ensure signal handlers are connected
        import family_ai_app.signals