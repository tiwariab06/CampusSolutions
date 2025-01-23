# Generated by Django 3.1.12 on 2024-12-17 13:27

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_auto_20241217_0015'),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name='students',
        #     name='email',
        #     field=models.EmailField(max_length=254, unique=True),
        # ),
        migrations.AlterField(
            model_name='students',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='students',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
