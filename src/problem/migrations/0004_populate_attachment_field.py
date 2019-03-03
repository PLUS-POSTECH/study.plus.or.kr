# Generated by Django 2.0.6 on 2018-06-21 08:08

import os
import pathlib
import shutil

from django.conf import settings
from django.db import migrations


def populate_attachment_field(apps, _):
    # noinspection PyPep8Naming
    ProblemAttachment = apps.get_model('problem', 'ProblemAttachment')

    delete_list = []

    for problem_attachment in ProblemAttachment.objects.all():
        reverse_relation = problem_attachment.old_problems
        if not reverse_relation.exists():
            delete_list.append(problem_attachment)
            continue

        problem_attachment.problem = reverse_relation.first()
        problem_attachment.save()

    attachments_path = os.path.join(settings.MEDIA_ROOT, 'attachments')
    previous_path = os.path.join(settings.MEDIA_ROOT, 'problem')
    pathlib.Path(attachments_path).mkdir(parents=True, exist_ok=True)
    if pathlib.Path(previous_path).exists():
        shutil.move(previous_path, attachments_path)

    for item in delete_list:
        item.delete()


def reverse_populate_attachment_field(apps, _):
    # noinspection PyPep8Naming
    ProblemAttachment = apps.get_model('problem', 'ProblemAttachment')

    for problem_attachment in ProblemAttachment.objects.all():
        problem_attachment.problem.attachments.add(problem_attachment)

    previous_path = os.path.join(settings.MEDIA_ROOT, 'attachments', 'problem')
    if pathlib.Path(previous_path).exists():
        shutil.move(previous_path, settings.MEDIA_ROOT)


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0003_auto_20180621_1707'),
    ]

    operations = [
        migrations.RunPython(populate_attachment_field, reverse_code=reverse_populate_attachment_field)
    ]
