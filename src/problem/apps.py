from django.apps import AppConfig


class ProblemConfig(AppConfig):
    name = 'problem'

    def ready(self):
        # pylint: disable=F401
        import problem.signals  # noqa: F401
