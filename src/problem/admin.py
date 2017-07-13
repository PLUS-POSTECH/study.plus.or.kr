from django.contrib import admin
from .models import *


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'categories_name', 'author', 'description')


@admin.register(ProblemAttachment)
class ProblemAttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', )


@admin.register(ProblemInstance)
class ProblemInstanceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'problem')


@admin.register(ProblemList)
class ProblemListAdmin(admin.ModelAdmin):
    list_display = ('title', 'session', 'description')
