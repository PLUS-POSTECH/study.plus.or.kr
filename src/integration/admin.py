from django.contrib import admin

from .models import Discord


@admin.register(Discord)
class DiscordAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['title', 'url_webhook', 'url_avatar', 'is_active']
        }),
        ('On First Blood', {
            'fields': ['on_first_blood', 'color_first_blood']
        }),
        ('On Solved', {
            'fields': ['on_solved', 'color_solved']
        }),
        ('On Problem Registered', {
            'fields': ['on_problem_registered', 'color_on_problem_registered']
        }),
        ('On Question', {
            'fields': ['on_question', 'color_on_question']
        }),
        ('On Answer', {
            'fields': ['on_answer', 'color_on_answer']
        })
    ]
