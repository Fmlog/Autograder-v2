# Generated by Django 4.0.5 on 2022-08-25 15:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grader', '0010_alter_assignment_id_alter_course_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='File',
            new_name='Submission',
        ),
    ]