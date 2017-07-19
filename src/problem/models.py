import os

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model

from website.models import Category, Session


User = get_user_model()


ProblemAttachmentStorage = FileSystemStorage(location=os.path.join('problem', 'attachments'))


class ProblemAttachment(models.Model):
    file = models.FileField(storage=ProblemAttachmentStorage)

    class Meta:
        verbose_name = '문제 첨부파일'
        verbose_name_plural = '문제 첨부파일들'

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return '%s' % self.filename()


class Problem(models.Model):
    title = models.CharField(max_length=50, unique=True)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User)
    description = models.TextField(blank=True)
    auth_key = models.TextField()
    last_modified = models.DateTimeField()
    attachments = models.ManyToManyField(ProblemAttachment, blank=True)

    class Meta:
        verbose_name = '문제'
        verbose_name_plural = '문제들'

    def categories_title(self):
        return ','.join(map(lambda x: x.title, self.categories.all()))

    def __str__(self):
        return '%s' % self.title


class ProblemList(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    session = models.ForeignKey(Session)

    class Meta:
        verbose_name = '문제 리스트'
        verbose_name_plural = '문제 리스트들'

    def __str__(self):
        return '%s' % self.title


class ProblemInstance(models.Model):
    problem = models.ForeignKey(Problem)
    problem_list = models.ForeignKey(ProblemList)
    points = models.IntegerField()
    distributed_points = models.IntegerField()
    breakthrough_points = models.IntegerField()
    hidden = models.BooleanField()

    class Meta:
        verbose_name = '문제 인스턴스'
        verbose_name_plural = '문제 인스턴스들'

    def __str__(self):
        return '%s' % self.problem.title


class ProblemAuthLog(models.Model):
    user = models.ForeignKey(User)
    problem_instance = models.ForeignKey(ProblemInstance)
    auth_key = models.TextField()
    datetime = models.DateTimeField()
