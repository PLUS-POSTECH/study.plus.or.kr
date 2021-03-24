from django.contrib import admin

from .models import Problem, ProblemAttachment, ProblemInstance, ProblemList, ProblemAuthLog, ProblemQuestion
from website.actions import ExportCsvMixin

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
class ProblemAuthLogAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('user', 'problem_instance', 'auth_key', 'datetime')
    actions = ['export_as_csv']


@admin.register(ProblemQuestion)
class ProblemQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem_instance', 'question', 'answer', 'datetime')
