import os
import mimetypes
from datetime import datetime

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, FileResponse, JsonResponse
from django.shortcuts import render
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

        def problems_gen(problems):
            for problem in problems:
                first_solved_log = None
                solved_log = ProblemAuthLog.objects.filter(problem_instance=problem,
                                                           auth_key=problem.problem.auth_key) \
                    .order_by('datetime') \
                    .distinct('user')

                if solved_log.exists():
                    first_solved_log = solved_log.first()
                authed = solved_log.filter(user=request.user).exists()
                solved_count = solved_log.count()
                first_blood = not first_solved_log or request.user == first_solved_log.user
                points = problem.points
                points += problem.distributed_points / (solved_count + (0 if authed else 1))
                points += problem.breakthrough_points if first_blood else 0
                yield (problem, points, authed, first_blood)

        problem_response = [(
                problem_list,
                problems_gen(problem_list.problem_instances.all())
            ) for problem_list in problem_lists
        ]

        return render(request, 'problem/list.html', {
            'sessions': all_sessions,
            'problem_lists': all_problem_lists,
            'queried_problem_lists': problem_response,
            'search_by': search_by,
            'q': q
        })


class ProblemGetForm(forms.Form):
    prob_id = forms.IntegerField(required=True)


class ProblemGetView(PlusMemberCheck, View):
    def get(self, request):
        form = ProblemGetForm(request.GET)
        if not form.is_valid():
            return HttpResponseBadRequest()

        problem_response = ProblemInstance.objects.get(pk=form.cleaned_data['prob_id'])
        first_solved_log = None
        solved_log = ProblemAuthLog.objects.filter(problem_instance=problem_response,
                                                   auth_key=problem_response.problem.auth_key) \
                                           .distinct() \
                                           .order_by('datetime')
        if solved_log.exists():
            first_solved_log = solved_log.first()
        authed = solved_log.filter(user=request.user).exists()
        solved_count = solved_log.count()

        problem = problem_response.problem
        points = problem.points
        points += problem.distributed_points / (solved_count + (0 if authed else 1))
        points += problem.breakthrough_points if first_solved_log.user == request.user else 0

        return render(request, 'problem/get.html', {
            'problem_instance': problem_response,
            'points': points,
            'solved_count': solved_count,
            'first_solved_log': first_solved_log,
            'authed': authed
        })


class ProblemAuthForm(forms.Form):
    prob_id = forms.IntegerField(required=True)
    auth_key = forms.CharField(required=True)


class ProblemAuthView(PlusMemberCheck, View):
    def post(self, request):
        form = ProblemAuthForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest()

        return_obj = {}
        prob_id = form.cleaned_data['prob_id']
        auth_key = form.cleaned_data['auth_key']
        try:
            problem_instance = ProblemInstance.objects.get(pk=prob_id)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest()

        ProblemAuthLog.objects.create(user=request.user,
                                      problem_instance=problem_instance,
                                      auth_key=auth_key,
                                      datetime=datetime.now())

        if problem_instance.problem.auth_key == auth_key:
            return_obj['result'] = True
        else:
            return_obj['result'] = False

        return JsonResponse(return_obj)


class DownloadForm(forms.Form):
    f = forms.IntegerField(required=True)


class DownloadView(PlusMemberCheck, View):
    def get(self, request):
        form = DownloadForm(request.GET)
        if not form.is_valid():
            return HttpResponseBadRequest()
        file_pk = form.cleaned_data['f']

        try:
            file = ProblemAttachment.objects.get(pk=file_pk).file
        except ObjectDoesNotExist:
            return HttpResponseBadRequest()

        file_name = os.path.basename(file.path)
        file_size = file.size

        response = FileResponse(file.open())
        content_type, encoding = mimetypes.guess_type(file_name)
        if content_type is None:
            content_type = 'application/octet-stream'
        if encoding is not None:
            response['Content-Encoding'] = encoding
        response['Content-Type'] = content_type
        response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % urlquote(file_name)
        response['Content-Length'] = str(file_size)
        return response
