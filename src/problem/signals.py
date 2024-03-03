from django.db.models.signals import post_save
from django.dispatch import receiver

from integration.helpers import discord
from .models import ProblemInstance, ProblemQuestion, ProblemAuthLog


# pylint: disable=W0613
@receiver(post_save, sender=ProblemInstance)
def on_update_problem_handler(sender, instance, **kwargs):
    discord.on_problem_updated(instance)


@receiver(post_save, sender=ProblemQuestion)
def on_question_handler(sender, instance: ProblemQuestion, **kwargs):
    if instance.answer == "":
        discord.on_question(instance)
    else:
        discord.on_answer(instance)


@receiver(post_save, sender=ProblemAuthLog)
def on_auth(sender, instance: ProblemAuthLog, **kwargs):
    if instance.auth_key == instance.problem_instance.problem.auth_key:
        problem_instance = instance.problem_instance
        if (
            ProblemAuthLog.objects.filter(
                problem_instance=problem_instance, auth_key=problem_instance.problem.auth_key
            ).count()
            == 1
        ):
            discord.on_first_blood(instance)
        else:
            discord.on_solved(instance)
    else:
        discord.on_auth_tried(instance)
