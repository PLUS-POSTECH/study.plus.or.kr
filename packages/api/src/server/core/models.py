from typing import TYPE_CHECKING

from django.contrib.auth.models import AbstractUser
from django.db import models

if TYPE_CHECKING:
    MetaProtocol = models.Model.Meta
else:
    MetaProtocol = object


class User(AbstractUser):
    povis_id = models.CharField(max_length=20, blank=True)
    is_plus_member = models.BooleanField(default=False)

    class Meta(MetaProtocol):
        verbose_name = "사용자"
        verbose_name_plural = "사용자들"


class Category(models.Model):
    title = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)

    class Meta(MetaProtocol):
        verbose_name = "카테고리"
        verbose_name_plural = "카테고리들"


class Session(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)

    class Meta(MetaProtocol):
        verbose_name = "분기"
        verbose_name_plural = "분기들"

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.title}>"


class Notification(MetaProtocol):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta(MetaProtocol):
        verbose_name = "공지사항"
        verbose_name_plural = "공지사항들"

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.title}>"
