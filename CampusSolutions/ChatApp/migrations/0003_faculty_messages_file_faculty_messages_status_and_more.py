# Generated by Django 5.2 on 2025-05-13 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatApp', '0002_faculty_messages_sent_at_student_messages_sent_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty_messages',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='chat_files/'),
        ),
        migrations.AddField(
            model_name='faculty_messages',
            name='status',
            field=models.CharField(choices=[('sent', 'Sent'), ('read', 'Read')], default='sent', max_length=10),
        ),
        migrations.AddField(
            model_name='student_messages',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='chat_files/'),
        ),
        migrations.AddField(
            model_name='student_messages',
            name='status',
            field=models.CharField(choices=[('sent', 'Sent'), ('read', 'Read')], default='sent', max_length=10),
        ),
    ]
