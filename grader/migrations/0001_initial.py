# Generated by Django 4.0.5 on 2022-09-28 21:15

from django.db import migrations, models
import django.db.models.deletion
import grader.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('file', models.FileField(upload_to=grader.models.get_config_upload_to)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('course_code', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('file', models.FileField(upload_to=grader.models.get_testcase_upload_to)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grader.assignment')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('file', models.FileField(upload_to=grader.models.get_sub_upload_to)),
                ('result', models.JSONField(default='{}')),
                ('grade', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grader.assignment')),
            ],
        ),
    ]
