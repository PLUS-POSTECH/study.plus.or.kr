from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    povis_id = models.CharField(max_length=20, blank=True)
    is_plus_member = models.BooleanField(default=False)


class ProblemCategory(models.Model):
    # TODO: Do Later
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()


class Problem(models.Model):
    # TODO: Do Later
    number = models.IntField(unique=True)
    category = models.ForeignKey(ProblemCategory)
    author = models.ForeignKey(User)
    description = models.TextField()
    key = models.TextField()
    last_modified = models.DateTimeField()
    points = models.IntField()
    distributed_points = models.IntField()
    attachment = models.FileField(upload_to='problem', null=True, blank=True)
    hidden = models.BooleanField()

admin.site.register(User)
