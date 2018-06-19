import os

from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model

from website.models import Category, Session


User = get_user_model()


# TODO: Use seminar_attachments or attachments/seminar
SeminarAttachmentStorage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'seminar'))


class SeminarAttachment(models.Model):
    # TODO: Use upload_to to generate storage folder (to remove name collision)
    file = models.FileField(storage=SeminarAttachmentStorage)

    class Meta:
        verbose_name = '세미나 첨부파일'
        verbose_name_plural = '세미나 첨부파일들'

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return '%s' % self.filename()


class Seminar(models.Model):
    title = models.CharField(max_length=50)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    session = models.ForeignKey(Session, on_delete=models.PROTECT)
    date = models.DateField()
    description = models.TextField(blank=True)
    attachments = models.ManyToManyField(SeminarAttachment, blank=True)

    class Meta:
        verbose_name = '세미나'
        verbose_name_plural = '세미나들'

    def categories_title(self):
        return ', '.join(map(lambda x: x.title, self.categories.all()))

    def __str__(self):
        return '%s' % self.title
