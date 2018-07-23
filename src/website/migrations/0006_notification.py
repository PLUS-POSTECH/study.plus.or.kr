# Generated by Django 2.0.7 on 2018-07-21 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_auto_20180621_1659'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
                ('isActive', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': '공지사항',
                'verbose_name_plural': '공지사항들',
            },
        ),
    ]