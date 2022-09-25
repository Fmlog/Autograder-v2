# Generated by Django 4.0.5 on 2022-08-17 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import grader.models
import home.softDelete
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
                ('language', models.CharField(blank=True, max_length=255, null=True)),
                ('lecturer', models.ForeignKey(blank=True, limit_choices_to={'is_lecturer': True}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', home.softDelete.SoftDeleteManager()),
            ],
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('file', models.FileField(upload_to=grader.models.get_testcase_upload_to)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grader.question')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', home.softDelete.SoftDeleteManager()),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('file', models.FileField(upload_to=grader.models.get_sub_upload_to)),
                ('result', models.JSONField(default='{}')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grader.question')),
            ],
        ),
    ]
