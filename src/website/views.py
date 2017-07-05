import os
from pathlib import Path

from django import forms
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.utils.encoding import smart_str
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


class PLUSMemberCheck(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_anonymous() and self.request.user.is_plus_member
    login_url = '/login'


class SeminarListForm(forms.Form):
    session = forms.CharField(required=False)


class SeminarListView(PLUSMemberCheck, View):
    def get(self, request):
        form = SeminarListForm(request.GET)
        sessions = Session.objects.filter(isActive=True).order_by('title')
        if form.is_valid() and form.cleaned_data['session']:
            # TODO: Add escape on delimiter or use the format on semantic ui.
            # Possible Security Concerns
            session_filter = form.cleaned_data['session'].split("|")
            sessions = Session.objects.filter(title__in=session_filter).order_by('title')

        seminar_dict = {session: Seminar.objects.filter(session=session).order_by('-date') for session in sessions}

        return render(request, 'seminar/list.html', {
            'seminar_dict': seminar_dict
        })


class DownloadForm(forms.Form):
    filename = forms.CharField(required=False)


class DownloadView(PLUSMemberCheck, View):
    def get(self, request):
        form = DownloadForm(request.GET)
        if not form.is_valid():
            raise Http404("Download Request Not Valid")
        filename = smart_str(form.cleaned_data['filename'])

        if DownloadView.download_filter(filename):
            raise Http404("Download Request Not Valid")

        size = Path(filename).stat().st_size
        response = FileResponse(open(filename, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.split(filename)[1]
        response['Content-Length'] = str(size)
        return response

    @staticmethod
    def download_filter(filename):
        split = os.path.split(filename)
        download_path_whitelist = ['problem_attachments', 'seminar_attachments']
        if split[0] not in download_path_whitelist:
            return True

        _, _, filenames = next(os.walk(split[0]), (None, None, []))
        if split[1] not in filenames:
            return True

        return False
