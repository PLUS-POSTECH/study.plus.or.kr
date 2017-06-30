import os
from pathlib import Path

from django import forms
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views import View
from django.http import FileResponse, Http404

from .models import User, Session, Seminar


# Create your views here.
def home(request):
    return render(request, 'index.html')


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
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                povis_id=form.cleaned_data['povis_id'],
            )
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'registration/register.html', {
                'form': form
            })


class SeminarListForm(forms.Form):
    s = forms.CharField(required=False)


def plus_member_check(user):
    return user.is_plus_member


class SeminarListView(View):
    @user_passes_test(plus_member_check, login_url='/login')
    def get(self, request):
        # TODO: Add seminar list template
        # form = SeminarListForm(request.GET)
        # session_filter = form.cleaned_data['s']
        # sessions = Session.objects.order_by('title')
        seminars = Seminar.objects.order_by('-date')
        # if session_filter != '':
        #     seminars = seminars.filter(session=session_filter)
        return render(request, 'seminar/list.html', {
            # 'sessions': sessions,
            'seminars': seminars
        })


class DownloadForm(forms.Form):
    filename = forms.CharField(required=False)


class DownloadView(View):
    @user_passes_test(plus_member_check, login_url='/login')
    def get(self, request):
        form = DownloadForm(request.GET)
        filename = form.cleaned_data['filename']

        if DownloadView.download_filter(filename):
            raise Http404("File Not Found")

        return FileResponse(open(filename))

    @staticmethod
    def download_filter(filename):
        split = os.path.split(filename)

        if not split[0] != 'problem_attachments' \
           and not split[0] != 'seminar_attachments':
            return True

        _, _, filenames = os.walk(split[0])
        if split[1] not in filenames:
            return True

        return False

