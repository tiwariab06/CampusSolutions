# Generated by Django 5.2 on 2025-05-05 17:59

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty_messages',
            name='sent_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 5, 17, 59, 31, 554786, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student_messages',
            name='sent_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
