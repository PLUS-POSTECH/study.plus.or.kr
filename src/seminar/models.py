import os

from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model

from website.models import Category, Session


User = get_user_model()


SeminarAttachmentStorage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'attachments', 'seminar'))


class Seminar(models.Model):
    title = models.CharField(max_length=50)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    session = models.ForeignKey(Session, on_delete=models.PROTECT)
    date = models.DateField()
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = '세미나'
        verbose_name_plural = '세미나들'

    def categories_title(self):
        return ', '.join(map(lambda x: x.title, self.categories.all()))

    def __str__(self):
        return '%s' % self.title


def upload_target(seminar_attachment, filename):
    return os.path.join(str(seminar_attachment.seminar.pk), filename)


class SeminarAttachment(models.Model):
    file = models.FileField(storage=SeminarAttachmentStorage, upload_to=upload_target)
    seminar = models.ForeignKey(Seminar, on_delete=models.PROTECT, related_name='seminar_attachments')

    class Meta:
        verbose_name = '세미나 첨부파일'
        verbose_name_plural = '세미나 첨부파일들'

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return '%s' % self.filename()
