# Generated by Django 4.0.5 on 2022-08-24 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.IntegerField(default=6861703, primary_key=True, serialize=False, unique=True),
        ),
    ]