from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    povis_id = models.CharField(max_length=20, blank=True)
    is_plus_member = models.BooleanField(default=False)


class Category(models.Model):
    # TODO: Do Later
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()


class ProblemAttachment(models.Model):
    file = models.FileField(upload_to='problem_attachments')


class Problem(models.Model):
    # TODO: Do Later
    number = models.IntField(unique=True)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User)
    description = models.TextField()
    key = models.TextField()
    last_modified = models.DateTimeField()
    points = models.IntField()
    distributed_points = models.IntField()
    attachments = models.ManyToManyField(ProblemAttachment)
    hidden = models.BooleanField()


class Session(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField


class SeminarAttachment(models.Model):
    file = models.FileField(upload_to='seminar_attachments')


class Seminar(models.Model):
    title = models.CharField(max_length=50)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User)
    session = models.ForeignKey(Session)
    date = models.DateField()
    description = models.TextField()
    attachments = models.ManyToManyField(SeminarAttachment)


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Problem)
admin.site.register(ProblemAttachment)
admin.site.register(Session)
admin.site.register(Seminar)
admin.site.register(SeminarAttachment)
