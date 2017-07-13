import os

from django.db import models
from django.contrib.auth import get_user_model

from website.models import Category


User = get_user_model()


class ProblemAttachment(models.Model):
    file = models.FileField(upload_to='problem/attachment')

    class Meta:
        verbose_name = '문제 첨부파일'
        verbose_name_plural = '문제 첨부파일들'

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return '%s' % self.filename()


class Problem(models.Model):
    title = models.CharField(max_length=50)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User)
    description = models.TextField(blank=True)
    auth_key = models.TextField()
    last_modified = models.DateTimeField()
    points = models.IntegerField()
    distributed_points = models.IntegerField()
    breakthrough_points = models.IntegerField()
    attachments = models.ManyToManyField(ProblemAttachment, blank=True)
    hidden = models.BooleanField()

    class Meta:
        verbose_name = '문제'
        verbose_name_plural = '문제들'

    def categories_name(self):
        return ','.join(map(lambda x: x.name, self.categories.all()))
