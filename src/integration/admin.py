from django.contrib import admin

from .models import Discord


@admin.register(Discord)
class DiscordAdmin(admin.ModelAdmin):
    pass
