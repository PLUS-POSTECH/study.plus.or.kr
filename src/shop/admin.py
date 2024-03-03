from datetime import datetime, timedelta

from django.contrib import admin

from .models import Shop, ShopItem, ShopPurchaseLog


class FilterShopPurchaseLogByPurchaseTime(admin.SimpleListFilter):
    title = "구매 시간"
    parameter_name = "purchase_time"

    SINCE_ONE_MONTH_AGO = "1M"
    SINCE_THREE_MONTHS_AGO = "3M"
    SINCE_SIX_MONTHS_AGO = "6M"
    SINCE_ONE_YEAR_AGO = "1Y"

    def lookups(self, request, model_admin):
        # (URL parameter, human-readable name)
        return (
            (self.SINCE_ONE_MONTH_AGO, "최근 1개월"),
            (self.SINCE_THREE_MONTHS_AGO, "최근 3개월"),
            (self.SINCE_SIX_MONTHS_AGO, "최근 6개월"),
            (self.SINCE_ONE_YEAR_AGO, "최근 1년"),
        )

    def queryset(self, request, queryset):
        if self.value() == self.SINCE_ONE_MONTH_AGO:
            return queryset.filter(
                purchase_time__gte=datetime.now() - timedelta(days=30)
            )
        if self.value() == self.SINCE_THREE_MONTHS_AGO:
            return queryset.filter(
                purchase_time__gte=datetime.now() - timedelta(days=30 * 3)
            )
        if self.value() == self.SINCE_SIX_MONTHS_AGO:
            return queryset.filter(
                purchase_time__gte=datetime.now() - timedelta(days=30 * 6)
            )
        if self.value() == self.SINCE_ONE_YEAR_AGO:
            return queryset.filter(
                purchase_time__gte=datetime.now() - timedelta(days=365)
            )


@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
    list_display = ("title", "hidden")
    readonly_fields = ("last_modified",)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("problem_list",)
    readonly_fields = ("last_modified",)


@admin.register(ShopPurchaseLog)
class ShopPurchaseLogAdmin(admin.ModelAdmin):
    list_display = ("user", "shop", "item", "succeed", "retrieved", "purchase_time")
    readonly_fields = ("purchase_time",)
    list_filter = ("succeed", "retrieved", FilterShopPurchaseLogByPurchaseTime)
