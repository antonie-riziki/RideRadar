from django.apps import AppConfig


class RideradarAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rideradar_app'
    
    def ready(self):
        """
        Import signals when the app is ready.
        This ensures signals are registered for the entire application.
        """
        import rideradar_app.signals  # noqa
