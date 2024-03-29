# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-06 12:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0002_auto_20170630_1943"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "카테고리", "verbose_name_plural": "카테고리들"},
        ),
        migrations.AlterModelOptions(
            name="problem",
            options={"verbose_name": "문제", "verbose_name_plural": "문제들"},
        ),
        migrations.AlterModelOptions(
            name="problemattachment",
            options={"verbose_name": "문제 첨부파일", "verbose_name_plural": "문제 첨부파일들"},
        ),
        migrations.AlterModelOptions(
            name="seminar",
            options={"verbose_name": "세미나", "verbose_name_plural": "세미나들"},
        ),
        migrations.AlterModelOptions(
            name="seminarattachment",
            options={"verbose_name": "세미나 첨부파일", "verbose_name_plural": "세미나 첨부파일들"},
        ),
        migrations.AlterModelOptions(
            name="session",
            options={"verbose_name": "분기", "verbose_name_plural": "분기들"},
        ),
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "사용자", "verbose_name_plural": "사용자들"},
        ),
        migrations.RenameField(
            model_name="category",
            old_name="name",
            new_name="title",
        ),
        migrations.AddField(
            model_name="session",
            name="isActive",
            field=models.BooleanField(default=False),
        ),
    ]
