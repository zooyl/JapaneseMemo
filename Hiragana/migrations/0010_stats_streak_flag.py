# Generated by Django 2.1.7 on 2019-04-29 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hiragana', '0009_stats_streak_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='stats',
            name='streak_flag',
            field=models.BooleanField(default=True),
        ),
    ]
