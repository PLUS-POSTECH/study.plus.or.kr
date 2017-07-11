from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    povis_id = models.CharField(max_length=20, blank=True)
    is_plus_member = models.BooleanField(default=False)

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'


