from django.contrib import admin
from .models import *


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(SeminarCategory)
class SeminarCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(Seminar)
class SeminarAdmin(admin.ModelAdmin):
    list_display = ('title', 'session', 'categories_title', 'author', 'description')


@admin.register(SeminarAttachment)
class SeminarAttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', )
