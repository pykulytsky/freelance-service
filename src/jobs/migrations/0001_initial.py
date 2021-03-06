# Generated by Django 3.1.3 on 2021-01-16 17:39

import authentication.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chat', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('title', models.CharField(max_length=1024, verbose_name='Job name')),
                ('description', models.CharField(max_length=8192)),
                ('deadline', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('is_price_fixed', models.BooleanField()),
                ('views', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_jobs', to=settings.AUTH_USER_MODEL)),
                ('chat_room', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='job', to='chat.room')),
                ('performer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='performed_jobs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('author', 'performer')},
            },
        ),
        migrations.CreateModel(
            name='FavoritesJobs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites_list', to='jobs.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites_jobs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AttachedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='files/')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='jobs.job')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('body', models.CharField(max_length=8192)),
                ('rating', models.PositiveSmallIntegerField(validators=[authentication.validators.rating_validator])),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_feedback', to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='jobs.job')),
                ('performer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_feedback', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('author', 'performer')},
            },
        ),
    ]
