from django import forms
from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views import View

from .models import User


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


class SeminarListView(View):
    def get(self, request):
        # TODO: Add seminar list template
        return render(request, 'seminar/list.html', {})
