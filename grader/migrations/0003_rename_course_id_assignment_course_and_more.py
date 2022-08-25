# Generated by Django 4.0.5 on 2022-08-24 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grader', '0002_assignment_course_remove_file_question_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='course_id',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='file',
            old_name='assignment_id',
            new_name='assignment',
        ),
        migrations.RenameField(
            model_name='testcase',
            old_name='assignment_id',
            new_name='assignment',
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='lecturer_id',
        ),
    ]
