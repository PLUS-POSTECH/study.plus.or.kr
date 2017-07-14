import os
import mimetypes
from pathlib import Path

from django import forms
from django.http import HttpResponseBadRequest, FileResponse, JsonResponse
from django.shortcuts import render
from django.utils.encoding import smart_str
from django.utils.http import urlquote
from django.views import View

from website.views import PlusMemberCheck
from website.models import Session
from .models import ProblemList, ProblemInstance


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
                first_blood = not problem.first_blood or request.user.username == problem.first_blood
                solved_users = problem.solved_users.all()
                authed = request.user in solved_users
                solved_count = len(solved_users)
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
        authed = request.user in problem_response.solved_users.all()

        return render(request, 'problem/get.html', {
            'problem': problem_response,
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
        problem_instance = ProblemInstance.objects.get(pk=prob_id)
        if problem_instance.problem.auth_key == auth_key:
            if request.user not in problem_instance.solved_users.all():
                if not problem_instance.first_blood:
                    setattr(problem_instance, 'first_blood', request.user.username)
                problem_instance.solved_users.add(request.user)
                problem_instance.save()
            return_obj['result'] = True
        else:
            return_obj['result'] = False

        return JsonResponse(return_obj)


class DownloadForm(forms.Form):
    filename = forms.CharField(required=True)


class DownloadView(PlusMemberCheck, View):
    def get(self, request):
        form = DownloadForm(request.GET)
        if not form.is_valid():
            return HttpResponseBadRequest()
        filename = smart_str(form.cleaned_data['filename'])

        if DownloadView.download_filter(filename):
            return HttpResponseBadRequest()

        file_path = 'problem' + os.path.sep + 'attachments' + os.path.sep + filename

        size = Path(file_path).stat().st_size
        response = FileResponse(open(file_path, 'rb'))
        content_type, encoding = mimetypes.guess_type(filename)
        if content_type is None:
            content_type = 'application/octet-stream'
        if encoding is not None:
            response['Content-Encoding'] = encoding
        response['Content-Type'] = content_type
        response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % urlquote(filename)
        response['Content-Length'] = str(size)
        return response

    @staticmethod
    def download_filter(filename):
        _, _, filenames = next(os.walk('problem' + os.path.sep + 'attachments'), (None, None, []))

        return filename not in filenames
