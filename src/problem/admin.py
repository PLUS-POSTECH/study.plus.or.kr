from django.contrib import admin

from .models import Problem, ProblemAttachment, ProblemInstance, ProblemList, ProblemAuthLog


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'categories_title', 'author', 'description')
    readonly_fields = ('last_modified', )


@admin.register(ProblemAttachment)
class ProblemAttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', )


@admin.register(ProblemInstance)
class ProblemInstanceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'problem')


@admin.register(ProblemList)
class ProblemListAdmin(admin.ModelAdmin):
    list_display = ('title', 'session', 'description')


@admin.register(ProblemAuthLog)
class ProblemAuthLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem_instance', 'auth_key', 'datetime')
