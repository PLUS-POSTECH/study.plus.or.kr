from integration.models import Discord
from problem.models import ProblemInstance
from django.contrib.auth import get_user_model

User = get_user_model()


def on_first_blood(_problem: ProblemInstance, _user: User):
    for bot in Discord.objects.filter(is_active=True, subscribe=_problem.problem_list, on_first_blood=True):
        bot.send_on_first_blood(_problem, _user)


def on_solved(_problem: ProblemInstance, _user: User):
    for bot in Discord.objects.filter(is_active=True, subscribe=_problem.problem_list, on_solved=True):
        bot.send_on_solved(_problem, _user)


def on_auth_tried(_problem: ProblemInstance, _user: User, _trial: str):
    for bot in Discord.objects.filter(is_active=True, subscribe=_problem.problem_list, on_auth_tried=True):
        print(bot.title)
        bot.send_on_auth_tried(_problem, _user, _trial)


def on_problem_registered(_problem: ProblemInstance):
    for bot in Discord.objects.filter(is_active=True, subscribe=_problem.problem_list, on_problem_registered=True):
        bot.send_on_problem_registered(_problem, _problem.problem.author, _problem.points)


def on_question(_problem: ProblemInstance, _user: User, _question: str):
    for bot in Discord.objects.filter(is_active=True, subscribe=_problem.problem_list, on_question=True):
        bot.send_on_question(_problem, _user, _question)


def on_answer(_problem: ProblemInstance, _user: User, _question: str, _answer: str):
    for bot in Discord.objects.filter(is_active=True, subscribe=_problem.problem_list, on_answer=True):
        bot.send_on_answer(_problem, _user, _question, _answer)
