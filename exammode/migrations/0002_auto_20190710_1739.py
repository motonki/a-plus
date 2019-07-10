# Generated by Django 2.2.3 on 2019-07-10 14:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('exammode', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='examsession',
            name='end_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='examsession',
            name='end_time_actual',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='examsession',
            name='may_leave_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='examsession',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='examsession',
            name='start_time_actual',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='examtaken',
            name='exam_finished',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
