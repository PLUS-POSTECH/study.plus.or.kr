from django.contrib import admin

from .models import ShopItem, Shop, ShopPurchaseLog


@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'hidden')
    readonly_fields = ('last_modified', )


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('problem_list', )
    readonly_fields = ('last_modified', )


@admin.register(ShopPurchaseLog)
class ShopPurchaseLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'shop', 'item', 'succeed', 'retrieved')
    readonly_fields = ('purchase_time', )