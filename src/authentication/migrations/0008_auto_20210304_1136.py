# Generated by Django 3.1.6 on 2021-03-04 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_auto_20210227_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Field updates when user login first time'),
        ),
    ]