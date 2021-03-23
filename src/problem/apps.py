from django.apps import AppConfig


class ProblemConfig(AppConfig):
    name = 'problem'

    def ready(self):
        import problem.signals
