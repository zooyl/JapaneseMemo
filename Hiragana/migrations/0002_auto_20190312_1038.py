# Generated by Django 2.1.7 on 2019-03-12 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hiragana', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='levels',
            name='answer',
        ),
        migrations.AlterField(
            model_name='levels',
            name='preset',
            field=models.IntegerField(choices=[(0, 'Easy'), (1, 'Medium'), (2, 'Hard')]),
        ),
    ]
