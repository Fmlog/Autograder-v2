# Generated by Django 4.0.5 on 2022-09-26 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grader', '0019_rename_grade_submission_score'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='score',
            new_name='grade',
        ),
    ]