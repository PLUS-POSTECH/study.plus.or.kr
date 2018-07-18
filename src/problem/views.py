import os
import mimetypes
from datetime import timedelta

from django import forms
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseBadRequest, HttpResponseServerError, FileResponse, JsonResponse
from django.shortcuts import render
from django.utils.http import urlquote
from django.views import View

from website.views import PlusMemberCheck
from website.models import Session, Category
from .models import ProblemList, ProblemInstance, ProblemAttachment, ProblemAuthLog, ProblemQuestion
from .helpers.score import AuthReplay
from .helpers.problem_info import get_problem_list_info, get_user_problem_info


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
        categories = Category.objects.order_by('title')
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
                notification_message = problem_list.notification
                yield problem_list, problem_info, notification_message, user_score

        queried_problem_lists = list(construct_response())

        return render(request, 'problem/list.html', {
            'sessions': all_sessions,
            'categories' : categories,
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

        return render(request, 'problem/get.html', {
            'info': get_user_problem_info(request.user, problem_instance)
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
            ProblemAuthLog.objects.create(
                user=request.user, problem_instance=problem_instance, auth_key=auth_key)
            is_correct = problem_instance.problem.auth_key == auth_key
            return_obj['result'] = is_correct

        except IntegrityError:
            return_obj['result'] = False

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


class ProblemRankView(PlusMemberCheck, View):
    def get(self, request, pk=None):
        problem_lists = ProblemList.objects
        if pk is None:
            sessions = Session.objects.filter(isActive=True).order_by('title')
            problem_lists = problem_lists.filter(session__in=sessions)
        else:
            problem_list_pk = int(pk)
            problem_lists = problem_lists.filter(pk=problem_list_pk)
            if not problem_lists.exists():
                raise Http404

        rank_info = []
        chart_info = []
        for problem_list in problem_lists:
            replay = AuthReplay(problem_list, timedelta(days=7))
            replay.prepare()
            top10_chart_data, top10_rank = replay.get_statistic_data()
            rank_info.append((problem_list, top10_rank))
            chart_info.append((problem_list, top10_chart_data))

        return render(request, 'problem/rank.html', {
            'rank_info': rank_info,
            'chart_info': chart_info
        })


class ProblemQuestionView(PlusMemberCheck, View):
    def get(self, request):
        questions = request.user.problemquestion_set.order_by('-datetime')
        answers = ProblemQuestion.objects.filter(problem_instance__problem__author=request.user).order_by('-datetime')

        return render(request, 'problem/question.html', {
            'queried_questions': questions,
            'queried_answers': answers
        })


class ProblemQuestionAskForm(forms.Form):
    question = forms.CharField(required=False)


class ProblemQuestionAskView(PlusMemberCheck, View):
    def post(self, request, pk):
        form = ProblemQuestionAskForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest()

        question_text = form.cleaned_data['question']

        try:
            problem_instance = ProblemInstance.objects.get(pk=int(pk))
        except ObjectDoesNotExist:
            raise Http404

        if not problem_instance.problem_list.allow_question:
            return HttpResponseBadRequest()

        question_response = {
            "name": problem_instance.problem.title,
            "list": problem_instance.problem_list.title,
            "question": question_text
        }

        if not question_text:
            question_response['ok'] = False
            return JsonResponse(question_response)

        else:
            question_response['ok'] = True

            try:
                ProblemQuestion.objects.create(
                    user=request.user, problem_instance=problem_instance, question=question_text)

            except BaseException:
                return HttpResponseServerError()

        return JsonResponse(question_response)
