from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ProblemInstance, ProblemQuestion
from integration.helpers import discord


@receiver(post_save, sender=ProblemInstance)
def on_register_problem_handler(sender, instance, **kwargs):
    discord.on_problem_registered(instance)


@receiver(post_save, sender=ProblemQuestion)
def on_question_handler(sender, instance: ProblemQuestion, **kwargs):
    print("wow")
    if instance.answer == "":
        discord.on_question(instance)
    else:
        discord.on_answer(instance)
