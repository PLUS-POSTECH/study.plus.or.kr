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


class Session(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    isActive = models.BooleanField(default=False)

    class Meta:
        verbose_name = '분기'
        verbose_name_plural = '분기들'

    def __str__(self):
        return '%s' % self.title


class Notification(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=False)
    isActive = models.BooleanField(default=True)
    datetime = models.DateTimeField()

    class Meta:
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항들'

    def __str__(self):
        return '%s' % self.title
