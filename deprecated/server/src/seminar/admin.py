from django.contrib import admin

from .models import Seminar, SeminarAttachment


@admin.register(Seminar)
class SeminarAdmin(admin.ModelAdmin):
    list_display = ('title', 'session', 'categories_title', 'author', 'description')


@admin.register(SeminarAttachment)
class SeminarAttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', )
