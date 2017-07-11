import os

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Session(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    isActive = models.BooleanField(default=False)

    class Meta:
        verbose_name = '분기'
        verbose_name_plural = '분기들'

    def __str__(self):
        return '%s' % self.title


class SeminarCategory(models.Model):
    title = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = '세미나 카테고리'
        verbose_name_plural = '세미나 카테고리들'

    def __str__(self):
        return '%s' % self.title


class SeminarAttachment(models.Model):
    file = models.FileField(upload_to='seminar_attachments')

    class Meta:
        verbose_name = '세미나 첨부파일'
        verbose_name_plural = '세미나 첨부파일들'

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return '%s' % self.filename()


class Seminar(models.Model):
    title = models.CharField(max_length=50)
    categories = models.ManyToManyField(SeminarCategory)
    author = models.ForeignKey(User)
    session = models.ForeignKey(Session)
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
