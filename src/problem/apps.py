from django.apps import AppConfig


class ProblemConfig(AppConfig):
    name = 'problem'

    def ready(self):
        # pylint: disable=C0415, W0611
        import problem.signals  # noqa: F401
