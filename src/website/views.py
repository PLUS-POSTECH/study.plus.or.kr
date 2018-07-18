from django import forms
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views import View

from .models import User


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
