# Generated by Django 2.0.7 on 2018-07-21 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_notification_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(),
        ),
    ]