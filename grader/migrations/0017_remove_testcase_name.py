# Generated by Django 4.0.5 on 2022-09-25 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grader', '0016_testcase_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testcase',
            name='name',
        ),
    ]