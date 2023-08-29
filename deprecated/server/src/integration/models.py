from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from problem.models import ProblemList, ProblemInstance, ProblemAuthLog

import requests

User = get_user_model()


class Discord(models.Model):
    title = models.CharField(max_length=100)
    url_webhook = models.URLField("Discord Webhook URL", max_length=300)
    url_avatar = models.URLField("Discord Avatar Image URL", max_length=400)

    is_active = models.BooleanField("Activation")

    on_first_blood = models.BooleanField("Send at First Blood")
    color_first_blood = models.CharField("Color of First Blood Message", max_length=50)

    on_solved = models.BooleanField("Send when Solved")
    color_solved = models.CharField("Color of Solved Message", max_length=50)

    on_auth_tried = models.BooleanField("Send at Any Trial")
    color_auth_tried = models.CharField("Color of Auth Trial Message", max_length=50)

    on_problem_registered = models.BooleanField("Send at Problem Instance Registered")
    color_on_problem_registered = models.CharField("Color of Plm Register Message", max_length=50)

    on_question = models.BooleanField("Send at Question")
    color_on_question = models.CharField("Color of Question Message", max_length=50)

    on_answer = models.BooleanField("Send at Answer")
    color_on_answer = models.CharField("Color of Answer Message", max_length=50)
    subscribe = models.ManyToManyField(ProblemList)

    class Meta:
        verbose_name = 'Discord Webhook 인스턴스'
        verbose_name_plural = 'Discord Webhook 인스턴스들'

    def __str__(self):
        return self.title

    def message(self, _title: str, _color: str, _problem: ProblemInstance, _user: User, _description: str = "", _fields=None):
        if _fields is None or type(_fields) != list:
            _fields = []

        return {
            "username": self.title,
            "avatar_url": self.url_avatar,
            "embeds": [{
                "title": _title,
                "color": _color,
                "fields": [{
                    "name": "Problem",
                    "value": _problem.problem.title
                }, {
                    "name": "User",
                    "value": _user.username
                }] + _fields,
                "description": _description,
                "timestamp": f"{timezone.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z"
            }]
        }

    def send_on_first_blood(self, _problem: ProblemAuthLog):
        requests.post(self.url_webhook, json=self.message(
            _title=":drop_of_blood: First Blood!",
            _color=self.color_first_blood,
            _problem=_problem.problem_instance,
            _user=_problem.user
        ))

    def send_on_solved(self, _problem: ProblemAuthLog):
        requests.post(self.url_webhook, json=self.message(
            _title=":triangular_flag_on_post: Solved!",
            _color=self.color_solved,
            _problem=_problem.problem_instance,
            _user=_problem.user
        ))

    def send_on_auth_tried(self, _problem: ProblemAuthLog):
        requests.post(self.url_webhook, json=self.message(
            _title=":x: Wrong!",
            _color=self.color_auth_tried,
            _problem=_problem.problem_instance,
            _user=_problem.user,
            _fields=[{
                "name": "Trial",
                "value": _problem.auth_key
            }]
        ))

    def send_on_problem_updated(self, _problem: ProblemInstance, _user: User, _point: int):
        requests.post(self.url_webhook, json=self.message(
            _title=":pushpin: Problem Updated!",
            _color=self.color_on_problem_registered,
            _problem=_problem,
            _user=_user,
            _fields=[{
                "name": "Points",
                "value": _point
            }, {
                "name": "Hidden",
                "value": ":o:" if _problem.hidden else ":x:"
            }]
        ))

    def send_on_question(self, _problem: ProblemInstance, _user: User, _question: str):
        requests.post(self.url_webhook, json=self.message(
            _title=":question: Question!",
            _color=self.color_on_problem_registered,
            _problem=_problem,
            _user=_user,
            _fields=[{
                "name": "Question",
                "value": _question
            }]
        ))

    def send_on_answer(self, _problem: ProblemInstance, _user: User, _question: str, _answer: str):
        requests.post(self.url_webhook, json=self.message(
            _title=":exclamation: Answered!",
            _color=self.color_on_problem_registered,
            _problem=_problem,
            _user=_user,
            _fields=[{
                "name": "Question",
                "value": _question
            }, {
                "name": "Answer",
                "value": _answer
            }]
        ))
