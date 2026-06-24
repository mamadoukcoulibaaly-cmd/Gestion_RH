from django.apps import AppConfig


class InformationEmployeesConfig(AppConfig):
    name = 'information_employees'

    def ready(self):
        # Ensure auth signal handlers are connected when the app is loaded.
        import information_employees.signals  # noqa: F401
