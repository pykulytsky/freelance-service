# Generated by Django 3.1.3 on 2021-01-28 21:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0003_auto_20210122_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favoritesjobs',
            name='job',
        ),
        migrations.AddField(
            model_name='favoritesjobs',
            name='job',
            field=models.ManyToManyField(related_name='favorites_list', to='jobs.Job'),
        ),
        migrations.AlterField(
            model_name='favoritesjobs',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='favorites_jobs', to=settings.AUTH_USER_MODEL),
        ),
    ]