# Generated by Django 3.2.12 on 2024-03-03 17:33
# Edited manually by f2koi@plus on the same date

from django.apps.registry import Apps
from django.db import migrations, models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

import shop.models as shop_models


def forwards_func(apps: Apps, schema_editor: BaseDatabaseSchemaEditor):
    ShopPurchaseLog: shop_models.ShopPurchaseLog = apps.get_model(
        "shop", "ShopPurchaseLog"
    )
    for log in ShopPurchaseLog.objects.all():
        log.purchased_price = log.item.price
        log.save()


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0004_shopitem_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="shoppurchaselog",
            name="purchased_price",
            field=models.PositiveIntegerField(default=0),
        ),
        # https://docs.djangoproject.com/en/3.2/ref/migration-operations/#runpython
        migrations.RunPython(
            code=forwards_func, reverse_code=migrations.RunPython.noop
        ),
    ]