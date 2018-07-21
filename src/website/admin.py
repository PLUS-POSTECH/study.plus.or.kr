from django.contrib import admin
from .models import User, Category, Session, Notification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


admin.site.register(Notification)