import os
import mimetypes
from pathlib import Path

from django import forms
from django.http import Http404, FileResponse
from django.shortcuts import render
from django.utils.encoding import smart_str
from django.utils.http import urlquote
from django.views import View

from website.views import PlusMemberCheck
from .models import Session, Seminar


class SeminarListForm(forms.Form):
    q = forms.CharField(required=False)
    search_by = forms.ChoiceField(required=False, choices=[
        ('', 'seminar'),
        ('seminar', 'seminar'),
        ('session', 'session')
    ])


class SeminarListView(PlusMemberCheck, View):
    def get(self, request):
        # TODO: Add Category Filter
        form = SeminarListForm(request.GET)
        if not form.is_valid():
            raise Http404("Invalid Seminar Request")

        all_sessions = Session.objects.order_by('title')
        all_seminars = Seminar.objects.order_by('title')
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
            'search_by': search_by,
            'q': q
        })


class DownloadForm(forms.Form):
    filename = forms.CharField(required=True)


class DownloadView(PlusMemberCheck, View):
    def get(self, request):
        form = DownloadForm(request.GET)
        if not form.is_valid():
            raise Http404("Download Request Not Valid")
        filename = smart_str(form.cleaned_data['filename'])

        if DownloadView.download_filter(filename):
            raise Http404("Download Request Not Valid")

        file_path = 'seminar' + os.path.sep + 'attachment' + os.path.sep + filename

        size = Path(file_path).stat().st_size
        response = FileResponse(open(file_path, 'rb'))
        content_type, encoding = mimetypes.guess_type(filename)
        if content_type is None:
            content_type = 'application/octet-stream'
        if encoding is not None:
            response['Content-Encoding'] = encoding
        response['Content-Type'] = content_type
        response['Content-Disposition'] = 'attachment; filename*="UTF-8\'\'%s"' % urlquote(filename)
        response['Content-Length'] = str(size)
        return response

    @staticmethod
    def download_filter(filename):
        _, _, filenames = next(os.walk('seminar_attachments'), (None, None, []))

        return filename not in filenames
