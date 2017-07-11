import os

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class ProblemCategory(models.Model):
    title = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = '문제 카테고리'
        verbose_name_plural = '문제 카테고리들'

    def __str__(self):
        return '%s' % self.title


class ProblemAttachment(models.Model):
    file = models.FileField(upload_to='problem_attachments')

    class Meta:
        verbose_name = '문제 첨부파일'
        verbose_name_plural = '문제 첨부파일들'

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return '%s' % self.filename()


class Problem(models.Model):
    number = models.IntegerField(unique=True)
    title = models.CharField(max_length=50)
    categories = models.ManyToManyField(ProblemCategory)
    author = models.ForeignKey(User)
    description = models.TextField(blank=True)
    key = models.TextField()
    last_modified = models.DateTimeField()
    points = models.IntegerField()
    distributed_points = models.IntegerField()
    attachments = models.ManyToManyField(ProblemAttachment, blank=True)
    hidden = models.BooleanField()

    class Meta:
        verbose_name = '문제'
        verbose_name_plural = '문제들'

    def categories_name(self):
        return ','.join(map(lambda x: x.name, self.categories.all()))
