# Generated by Django 2.0.7 on 2018-08-31 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20180831_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='no_of_attempts',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='question',
            name='word_limit',
            field=models.IntegerField(default=150),
        ),
    ]
