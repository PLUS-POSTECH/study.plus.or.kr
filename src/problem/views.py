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


class ProblemListForm(forms.Form):
    sort_by = forms.ChoiceField(required=False, choices=[
        ('', 'number'),
        ('number', 'number'),
        ('category', 'category')
    ])


class ProblemListView(PlusMemberCheck, View):
    def get(self, request):
        # TODO: Implement this
        raise Http404('Not Implemented')


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

        file_path = 'problem_attachments' + os.path.sep + filename

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
        _, _, filenames = next(os.walk('problem_attachments'), (None, None, []))

        return filename not in filenames
