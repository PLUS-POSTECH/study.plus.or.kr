import os

from django.db import models
from django.contrib.auth import get_user_model

from website.models import Category, Session


User = get_user_model()


class ProblemAttachment(models.Model):
    file = models.FileField(upload_to='problem' + os.path.sep + 'attachments')

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
    attachments = models.ManyToManyField(ProblemAttachment, blank=True)

    class Meta:
        verbose_name = '문제'
        verbose_name_plural = '문제들'

    def categories_title(self):
        return ','.join(map(lambda x: x.title, self.categories.all()))

    def __str__(self):
        return '%s' % self.title


class ProblemInstance(models.Model):
    problem = models.ForeignKey(Problem)
    points = models.IntegerField()
    distributed_points = models.IntegerField()
    breakthrough_points = models.IntegerField()
    first_blood = models.CharField(max_length=150, blank=True)
    solved_users = models.ManyToManyField(User, blank=True)
    hidden = models.BooleanField()

    class Meta:
        verbose_name = '문제 인스턴스'
        verbose_name_plural = '문제 인스턴스들'

    def solved_count(self):
        return len(self.solved_users.all())

    def __str__(self):
        return '%s' % self.problem.title


class ProblemList(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    session = models.ForeignKey(Session)
    problem_instances = models.ManyToManyField(ProblemInstance)

    class Meta:
        verbose_name = '문제 리스트'
        verbose_name_plural = '문제 리스트들'

    def __str__(self):
        return '%s' % self.title
