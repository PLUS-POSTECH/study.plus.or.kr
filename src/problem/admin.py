from django.contrib import admin
from .models import *


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'categories_name', 'author', 'description')


@admin.register(ProblemAttachment)
class ProblemAttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', )
