# Generated by Django 2.1.7 on 2019-03-31 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0008_problemlist_announcement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemauthlog',
            name='problem_instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.ProblemInstance'),
        ),
    ]
