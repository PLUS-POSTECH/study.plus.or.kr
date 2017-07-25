import os
import json
import mimetypes
from datetime import timedelta
from functools import reduce

from django import forms
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, FileResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.http import urlquote
from django.views import View

from website.views import PlusMemberCheck
from website.models import Session
from .models import ProblemList, ProblemInstance, ProblemAttachment, ProblemAuthLog


class ProblemListForm(forms.Form):
    q = forms.CharField(required=False)
    search_by = forms.ChoiceField(required=False, choices=[
        ('list_title', 'list title'),
        ('session', 'session')
    ])


class ProblemListView(PlusMemberCheck, View):
    def get(self, request):
        form = ProblemListForm(request.GET)
        if not form.is_valid():
            return HttpResponseBadRequest()

        all_sessions = Session.objects.order_by('title')
        all_problem_lists = ProblemList.objects.order_by('title')
        sessions = all_sessions.filter(isActive=True)
        problem_lists = all_problem_lists
        q = ''
        search_by = 'list_title'
        if form.cleaned_data['q']:
            if form.cleaned_data['search_by']:
                search_by = form.cleaned_data['search_by']
            q = form.cleaned_data['q']

            if search_by == "list_title":
                problem_lists = problem_lists.filter(title__search=q)
            elif search_by == "session":
                sessions = sessions.filter(title__search=q)
                problem_lists = problem_lists.filter(session__in=sessions)
        else:
            problem_lists = problem_lists.filter(session__in=sessions)

        def problem_list_info(problem_list):
            problem_instances = ProblemInstance.objects.filter(problem_list=problem_list)
            problem_info = []
            total_score = 0
            for problem_instance in problem_instances:
                first_solved_log = None
                solved_log = ProblemAuthLog.objects.filter(problem_instance=problem_instance,
                                                           auth_key=problem_instance.problem.auth_key) \
                                                   .order_by('datetime')

                if solved_log.exists():
                    first_solved_log = solved_log.first()
                authed = solved_log.filter(user=request.user).exists()
                solved_count = solved_log.count()
                first_blood = not first_solved_log or request.user == first_solved_log.user
                points = problem_instance.points
                points += problem_instance.distributed_points / (solved_count + (0 if authed else 1))
                points += problem_instance.breakthrough_points if first_blood else 0
                if authed:
                    total_score += points
                problem_info.append((problem_instance, int(points), authed, first_blood))

            return problem_list, problem_info, int(total_score)

        problem_response = [
            problem_list_info(problem_list)
            for problem_list in problem_lists
        ]

        return render(request, 'problem/list.html', {
            'sessions': all_sessions,
            'problem_lists': all_problem_lists,
            'queried_problem_lists': problem_response,
            'search_by': search_by,
            'q': q
        })


class ProblemGetView(PlusMemberCheck, View):
    def get(self, request, pk):
        try:
            problem_response = ProblemInstance.objects.get(pk=int(pk))
        except ObjectDoesNotExist:
            return HttpResponseBadRequest()

        first_solved_log = None
        solved_log = ProblemAuthLog.objects.filter(problem_instance=problem_response,
                                                   auth_key=problem_response.problem.auth_key) \
                                           .order_by('datetime')
        if solved_log.exists():
            first_solved_log = solved_log.first()
        authed = solved_log.filter(user=request.user).exists()
        solved_count = solved_log.count()

        points = problem_response.points
        points += problem_response.distributed_points / (solved_count + (0 if authed else 1))
        points += problem_response.breakthrough_points if not first_solved_log or first_solved_log.user == request.user else 0

        return render(request, 'problem/get.html', {
            'problem_instance': problem_response,
            'points': int(points),
            'solved_count': solved_count,
            'first_solved_log': first_solved_log,
            'authed': authed
        })


class ProblemAuthForm(forms.Form):
    auth_key = forms.CharField(required=True)


class ProblemAuthView(PlusMemberCheck, View):
    def post(self, request, pk):
        form = ProblemAuthForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest()

        return_obj = {}
        prob_id = int(pk)
        auth_key = form.cleaned_data['auth_key']
        try:
            problem_instance = ProblemInstance.objects.get(pk=prob_id)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest()

        try:
            ProblemAuthLog.objects.create(user=request.user,
                                          problem_instance=problem_instance,
                                          auth_key=auth_key,
                                          datetime=timezone.now())
            if problem_instance.problem.auth_key == auth_key:
                return_obj['result'] = True
            else:
                return_obj['result'] = False
        except IntegrityError:
            return_obj['result'] = False

        finally:
            return JsonResponse(return_obj)


class DownloadForm(forms.Form):
    f = forms.IntegerField(required=True)


class DownloadView(PlusMemberCheck, View):
    def get(self, request, pk):
        try:
            file_obj = ProblemAttachment.objects.get(pk=int(pk)).file
        except ObjectDoesNotExist:
            return HttpResponseBadRequest()

        file_name = os.path.basename(file_obj.path)
        file_size = file_obj.size

        response = FileResponse(file_obj)
        content_type, encoding = mimetypes.guess_type(file_name)
        if content_type is None:
            content_type = 'application/octet-stream'
        if encoding is not None:
            response['Content-Encoding'] = encoding
        response['Content-Type'] = content_type
        response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % urlquote(file_name)
        response['Content-Length'] = str(file_size)
        return response


class ProblemRankView(PlusMemberCheck, View):
    def get(self, request, pk=-1):
        problem_list_id = int(pk)

        problem_lists = ProblemList.objects
        if problem_list_id == -1:
            sessions = Session.objects.filter(isActive=True).order_by('title')
            problem_lists = problem_lists.filter(session__in=sessions)
        else:
            problem_lists = problem_lists.filter(pk=problem_list_id)
            if not problem_lists.exists():
                return HttpResponseBadRequest()

        def auth_replay(problems):
            user_info = {}
            problem_info = {}
            problem_instances = ProblemInstance.objects.filter(problem_list=problems)
            datetime_std = timezone.now() - timedelta(days=7)
            for problem_instance in problem_instances:
                problem_key = problem_instance.pk
                first_solved_log = None
                solved_logs = ProblemAuthLog.objects.filter(problem_instance=problem_instance,
                                                            auth_key=problem_instance.problem.auth_key,
                                                            datetime__lt=datetime_std) \
                    .order_by('datetime')

                if solved_logs.exists():
                    first_solved_log = solved_logs.first()
                solved_count = solved_logs.count()

                first_blood = None if not first_solved_log else first_solved_log.user
                problem = ((problem_instance.points,
                            problem_instance.distributed_points,
                            problem_instance.breakthrough_points),
                           solved_count,
                           first_blood)
                problem_info[problem_key] = problem

                for solved_log in solved_logs:
                    user_object = solved_log.user
                    solved_problems, last_auth = user_info.get(user_object, ([], None))
                    solved_problems = solved_problems + [problem_key]
                    if not last_auth or last_auth < solved_log.datetime:
                        last_auth = solved_log.datetime
                    user_info[user_object] = solved_problems, last_auth

            logs_to_play = [] if not problem_instances else \
                reduce(lambda x, y: x | y,
                       [ProblemAuthLog.objects.filter(problem_instance=problem_instance,
                                                      auth_key=problem_instance.problem.auth_key,
                                                      datetime__gte=datetime_std)
                        for problem_instance in problem_instances]).order_by('datetime')

            yield datetime_std, user_info.copy(), problem_info.copy()

            for log in logs_to_play:
                user_object = log.user
                problem_key = log.problem_instance.pk
                points, solved_count, first_blood = problem_info[problem_key]
                solved_count += 1
                if first_blood is None:
                    first_blood = user_object

                solved_problems, last_auth = user_info.get(user_object, ([], None))
                solved_problems = solved_problems + [problem_key]
                last_auth = log.datetime
                user_info[user_object] = solved_problems, last_auth

                problem_info[problem_key] = points, solved_count, first_blood

                yield log.datetime, user_info.copy(), problem_info.copy()

        rank_info = []
        chart_info = []
        rank_raw = []
        for problem_list in problem_lists:
            replay_data = auth_replay(problem_list)

            chart_data = {}
            for cur_datetime, user_data, problem_data in replay_data:
                def process_user_data(user_entry):
                    user_object, (solved_problems, last_auth) = user_entry

                    def calc_point(problem_key):
                        points, solved_count, first_blood = problem_data[problem_key]
                        user_first_blood = 0 if not first_blood or first_blood != user_entry[0] else 1
                        return int(points[0] + (points[1] / solved_count) + (points[2] * user_first_blood))

                    user_points = map(calc_point, solved_problems)
                    return user_object.username, sum(user_points), last_auth

                rank_raw = list(map(process_user_data, user_data.items()))
                for username, score, _ in rank_raw:
                    entry = chart_data.get(username, [])
                    entry.append({'x': cur_datetime.isoformat(), 'y': score})
                    chart_data[username] = entry

            rank_sorted = sorted(rank_raw, key=lambda x: (x[1], x[2]))[:10]
            rankers = map(lambda x: x[0], rank_sorted)
            chart_entry = filter(lambda x: x[0] in rankers,
                                 map(lambda x: (x[0], json.dumps(x[1])),
                                     chart_data.items()))
            rank_info.append((problem_list, rank_sorted))
            chart_info.append((problem_list.pk, chart_entry))

        return render(request, 'problem/rank.html', {
            'rank_info': rank_info,
            'chart_info': chart_info
        })


class ProblemQuestionView(PlusMemberCheck, View):
    def get(self, request):
        return render(request, 'problem/question.html')
