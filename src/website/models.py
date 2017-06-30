import os

from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    povis_id = models.CharField(max_length=20, blank=True)
    is_plus_member = models.BooleanField(default=False)


class Category(models.Model):
    # TODO: Do Later
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s' % self.name


class ProblemAttachment(models.Model):
    file = models.FileField(upload_to='problem_attachments')

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return '%s' % self.filename()


class Problem(models.Model):
    # TODO: Do Later
    number = models.IntegerField(unique=True)
    title = models.CharField(max_length=50)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User)
    description = models.TextField(blank=True)
    key = models.TextField()
    last_modified = models.DateTimeField()
    points = models.IntegerField()
    distributed_points = models.IntegerField()
    attachments = models.ManyToManyField(ProblemAttachment)
    hidden = models.BooleanField()

    def categories_name(self):
        return ','.join(map(lambda x: x.name, self.categories.all()))


class Session(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s' % self.title


class SeminarAttachment(models.Model):
    file = models.FileField(upload_to='seminar_attachments')

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
    description = models.TextField()
    attachments = models.ManyToManyField(SeminarAttachment)

    def categories_name(self):
        return ','.join(map(lambda x: x.name, self.categories.all()))

    def __str__(self):
        return '%s' % self.title
