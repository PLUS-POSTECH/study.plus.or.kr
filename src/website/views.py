from django import forms
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views import View
from .models import User, Notification
from problem.models import ProblemAuthLog, ProblemInstance
from functools import reduce


def home(request):
    all_notifications = Notification.objects.order_by('-date')

    solved_log_queries = []
    first_solved_logs = []
    for problem_instance in ProblemInstance.objects.all():
        correct_auth_key = problem_instance.problem.auth_key
        solve_logs = ProblemAuthLog.objects.filter(problem_instance=problem_instance, auth_key=correct_auth_key) \
            .order_by('-datetime')
        solved_log_queries.append(solve_logs)
        if solve_logs.exists():
            first_solved_logs.append(solve_logs.last())

    recent_solves = reduce(lambda x, y: x | y, solved_log_queries, ProblemAuthLog.objects.none()) \
        .order_by('-datetime')[:10]

    return render(request, 'index.html', {
        'notifications': all_notifications,
        'recent_solves': recent_solves,
        'first_solves': first_solved_logs
    })


def validate_unique_username(value):
    if User.objects.filter(username__iexact=value).count() > 0:
        raise ValidationError(
            _('username already exist')
        )


class RegisterForm(forms.Form):
    username = forms.CharField(validators=[validate_unique_username])
    password = forms.CharField(min_length=8)
    email = forms.EmailField()
    povis_id = forms.CharField(required=False)


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration/register.html', {
            'form': form
        })

    def post(self, request):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return render(request, 'registration/register.html', {
                'form': form
            })

        user = User.objects.create_user(
            form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            povis_id=form.cleaned_data['povis_id'],
        )
        login(request, user)
        return redirect('/')


class PlusMemberCheck(UserPassesTestMixin):
    # pylint: disable=no-member
    def test_func(self):
        return not self.request.user.is_anonymous and self.request.user.is_plus_member
    login_url = '/login'
