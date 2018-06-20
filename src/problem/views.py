import os
import mimetypes
from datetime import timedelta

from django import forms
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseBadRequest, FileResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.http import urlquote
from django.views import View

from website.views import PlusMemberCheck
from website.models import Session
from .models import ProblemList, ProblemInstance, ProblemAttachment, ProblemAuthLog
from .helpers.score import get_problem_list_info, AuthReplay


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

        def construct_response():
            for problem_list in problem_lists:
                problem_info, user_score = get_problem_list_info(problem_list, request.user)
                yield problem_list, problem_info, user_score

        queried_problem_lists = construct_response()

        return render(request, 'problem/list.html', {
            'sessions': all_sessions,
            'problem_lists': all_problem_lists,
            'queried_problem_lists': queried_problem_lists,
            'search_by': search_by,
            'q': q
        })


class ProblemGetView(PlusMemberCheck, View):
    def get(self, request, pk):
        try:
            problem_instance = ProblemInstance.objects.get(pk=int(pk))
        except ObjectDoesNotExist:
            raise Http404

        solved_log = ProblemAuthLog.objects \
            .filter(problem_instance=problem_instance, auth_key=problem_instance.problem.auth_key) \
            .order_by('datetime')

        first_solved_log = solved_log.first() if solved_log.exists() else None
        solved = solved_log.filter(user=request.user).exists()
        solved_count = solved_log.count()

        effective_solved_count = solved_count + (0 if solved else 1)
        effective_distributed_points = problem_instance.distributed_points / effective_solved_count
        breakthrough_relevant = first_solved_log is None or first_solved_log.user == request.user
        points = problem_instance.points
        points += effective_distributed_points
        points += problem_instance.breakthrough_points if breakthrough_relevant else 0

        problem_attachments = ProblemAttachment.objects.filter(problem=problem_instance.problem)

        return render(request, 'problem/get.html', {
            'problem_instance': problem_instance,
            'problem_attachments': problem_attachments,
            'points': int(points),
            'solved_count': solved_count,
            'first_solved_log': first_solved_log,
            'solved': solved
        })


class ProblemAuthForm(forms.Form):
    auth_key = forms.CharField(required=False)


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
            raise Http404

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


class ProblemDownloadView(PlusMemberCheck, View):
    def get(self, request, pk):
        try:
            file_obj = ProblemAttachment.objects.get(pk=int(pk)).file
        except ObjectDoesNotExist:
            raise Http404

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


# TODO: FIX latency using Django cache.
class ProblemRankView(PlusMemberCheck, View):
    def get(self, request, pk=None):
        problem_list_id = int(pk)

        problem_lists = ProblemList.objects
        if problem_list_id is None:
            sessions = Session.objects.filter(isActive=True).order_by('title')
            problem_lists = problem_lists.filter(session__in=sessions)
        else:
            problem_lists = problem_lists.filter(pk=problem_list_id)
            if not problem_lists.exists():
                raise Http404

        rank_info = []
        chart_info = []
        for problem_list in problem_lists:
            replay = AuthReplay(problem_list, timedelta(days=7))
            replay.crunch()
            top10_chart_data, top10_rank = replay.get_statistic_data()
            rank_info.append((problem_list, top10_rank))
            chart_info.append((problem_list.pk, top10_chart_data))

        return render(request, 'problem/rank.html', {
            'rank_info': rank_info,
            'chart_info': chart_info
        })


class ProblemQuestionView(PlusMemberCheck, View):
    def get(self, request):
        return render(request, 'problem/question.html')
