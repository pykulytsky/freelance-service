# Generated by Django 3.1.3 on 2021-01-29 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_job_published'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favoritesjobs',
            old_name='job',
            new_name='jobs',
        ),
    ]
