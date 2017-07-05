import os

from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    povis_id = models.CharField(max_length=20, blank=True)
    is_plus_member = models.BooleanField(default=False)

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'


class Category(models.Model):
    title = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리들'

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
    categories = models.ManyToManyField(Category)
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


class Session(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    isActive = models.BooleanField(default=False)

    class Meta:
        verbose_name = '분기'
        verbose_name_plural = '분기들'

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
    categories = models.ManyToManyField(Category)
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
