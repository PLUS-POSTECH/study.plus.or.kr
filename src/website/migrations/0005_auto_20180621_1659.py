# Generated by Django 2.0.6 on 2018-06-21 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0004_auto_20170713_2346"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(blank=True, max_length=150, verbose_name="last name"),
        ),
    ]
