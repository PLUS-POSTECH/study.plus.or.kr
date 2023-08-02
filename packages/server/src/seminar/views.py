import os
import mimetypes

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, FileResponse
from django.shortcuts import render
from django.utils.http import urlquote
from django.views import View
from website.models import Category
from website.views import PlusMemberCheck
from .models import Session, Seminar, SeminarAttachment


class SeminarListForm(forms.Form):
    q = forms.CharField(required=False)
    search_by = forms.ChoiceField(required=False, choices=[
        ('', 'seminar'),
        ('seminar', 'seminar'),
        ('session', 'session')
    ])


class SeminarListView(PlusMemberCheck, View):
    def get(self, request):
        form = SeminarListForm(request.GET)
        if not form.is_valid():
            return HttpResponseBadRequest()

        all_sessions = Session.objects.order_by('title')
        all_seminars = Seminar.objects.order_by('title')
        categories = Category.objects.order_by('title')
        sessions = all_sessions
        seminars = Seminar.objects.order_by('session', '-date')
        q = ''
        search_by = 'seminar'
        if form.cleaned_data['q']:
            if form.cleaned_data['search_by']:
                search_by = form.cleaned_data['search_by']
            q = form.cleaned_data['q']

            if search_by == "seminar":
                seminars = seminars.filter(title__search=q)
                sessions = sessions.filter(pk__in=seminars.values_list('session', flat=True).distinct())
            elif search_by == "session":
                sessions = sessions.filter(title__search=q)
        else:
            sessions = sessions.filter(isActive=True)

        seminar_dict = {session: seminars.filter(session=session) for session in sessions}

        return render(request, 'seminar/list.html', {
            'sessions': all_sessions,
            'seminars': all_seminars,
            'seminar_dict': seminar_dict,
            'categories': categories,
            'search_by': search_by,
            'q': q
        })


class SeminarDownloadView(PlusMemberCheck, View):
    def get(self, request, pk):
        try:
            file_obj = SeminarAttachment.objects.get(pk=int(pk)).file
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
