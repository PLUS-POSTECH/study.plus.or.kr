from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'description')


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    fields = ('title', 'categories', 'author', 'description')


@admin.register(ProblemAttachment)
class ProblemAttachmentAdmin(admin.ModelAdmin):
    fields = 'filename'


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    fields = ('title', 'description')


@admin.register(Seminar)
class SeminarAdmin(admin.ModelAdmin):
    fields = ('title', 'categories', 'author', 'description')


@admin.register(SeminarAttachment)
class SeminarAttachmentAdmin(admin.ModelAdmin):
    fields = 'filename'
