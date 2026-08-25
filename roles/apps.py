from django.apps import AppConfig


class RolesConfig(AppConfig):
    name = 'roles'

    def ready(self) -> None:
        from . import signals
