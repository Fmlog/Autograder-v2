# Generated by Django 4.0.5 on 2022-09-25 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grader', '0015_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcase',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
