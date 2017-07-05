from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'categories_name', 'author', 'description')


@admin.register(ProblemAttachment)
class ProblemAttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', )


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(Seminar)
class SeminarAdmin(admin.ModelAdmin):
    list_display = ('title', 'session', 'categories_title', 'author', 'description')


@admin.register(SeminarAttachment)
class SeminarAttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', )
