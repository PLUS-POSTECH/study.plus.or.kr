from integration.models import Discord
from problem.models import ProblemInstance, ProblemQuestion, ProblemAuthLog
from django.contrib.auth import get_user_model

User = get_user_model()


def on_first_blood(_problem: ProblemAuthLog):
    for bot in Discord.objects.filter(is_active=True, subscribe=_problem.problem_instance.problem_list, on_first_blood=True):
        bot.send_on_first_blood(_problem)


def on_solved(_problem: ProblemAuthLog):
    for bot in Discord.objects.filter(is_active=True, subscribe=_problem.problem_instance.problem_list, on_solved=True):
        bot.send_on_solved(_problem)


def on_auth_tried(_problem: ProblemAuthLog):
    for bot in Discord.objects.filter(is_active=True, subscribe=_problem.problem_instance.problem_list, on_auth_tried=True):
        print(bot.title)
        bot.send_on_auth_tried(_problem)


def on_problem_updated(_problem: ProblemInstance):
    for bot in Discord.objects.filter(is_active=True, subscribe=_problem.problem_list, on_problem_registered=True):
        bot.send_on_problem_updated(_problem, _problem.problem.author, _problem.points)


def on_question(_question: ProblemQuestion):
    for bot in Discord.objects.filter(is_active=True, subscribe=_question.problem_instance.problem_list, on_question=True):
        bot.send_on_question(_question.problem_instance, _question.user, _question.question)


def on_answer(_question: ProblemQuestion):
    for bot in Discord.objects.filter(is_active=True, subscribe=_question.problem_instance.problem_list, on_answer=True):
        bot.send_on_answer(_question.problem_instance, _question.user, _question.question, _question.answer)
