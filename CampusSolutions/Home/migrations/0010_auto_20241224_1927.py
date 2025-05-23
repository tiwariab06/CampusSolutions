# Generated by Django 3.1.12 on 2024-12-24 13:57

import datetime
from django.db import migrations, models


utc = datetime.timezone.utc


class Migration(migrations.Migration):

    dependencies = [
        ("Home", "0009_auto_20241223_0103"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendance",
            name="date",
            field=models.DateField(
                default=datetime.datetime(2024, 12, 24, 13, 57, 58, 74262, tzinfo=utc)
            ),
        ),
        migrations.AlterField(
            model_name="attendance",
            name="status",
            field=models.CharField(max_length=50),
        ),
        # migrations.AlterField(
        #     model_name='students',
        #     name='email',
        #     field=models.EmailField(max_length=254, unique=True),
        # ),
        # migrations.AlterField(
        #     model_name='students',
        #     name='roll_number',
        #     field=models.CharField(max_length=50, unique=True),
        # ),
    ]
