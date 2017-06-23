from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    povis_id = models.CharField(max_length=20, blank=True)
    is_plus_member = models.BooleanField(default=False)

admin.site.register(User)
