# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 10:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("name", models.CharField(max_length=30, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Problem",
            fields=[
                (
                    "id",
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("number", models.IntegerField(unique=True)),
                ("title", models.CharField(max_length=50)),
                ("description", models.TextField(blank=True)),
                ("key", models.TextField()),
                ("last_modified", models.DateTimeField()),
                ("points", models.IntegerField()),
                ("distributed_points", models.IntegerField()),
                ("hidden", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="ProblemAttachment",
            fields=[
                (
                    "id",
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("file", models.FileField(upload_to="problem_attachments")),
            ],
        ),
        migrations.CreateModel(
            name="Seminar",
            fields=[
                (
                    "id",
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("title", models.CharField(max_length=50)),
                ("date", models.DateField()),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="SeminarAttachment",
            fields=[
                (
                    "id",
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("file", models.FileField(upload_to="seminar_attachments")),
            ],
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "id",
                    models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("title", models.CharField(max_length=50, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name="seminar",
            name="attachments",
            field=models.ManyToManyField(blank=True, to="website.SeminarAttachment"),
        ),
        migrations.AddField(
            model_name="seminar",
            name="author",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="seminar",
            name="categories",
            field=models.ManyToManyField(to="website.Category"),
        ),
        migrations.AddField(
            model_name="seminar",
            name="session",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="website.Session"),
        ),
        migrations.AddField(
            model_name="problem",
            name="attachments",
            field=models.ManyToManyField(blank=True, to="website.ProblemAttachment"),
        ),
        migrations.AddField(
            model_name="problem",
            name="author",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="problem",
            name="categories",
            field=models.ManyToManyField(to="website.Category"),
        ),
    ]
