# Generated by Django 2.1.7 on 2019-04-28 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hiragana', '0007_auto_20190412_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stats',
            name='streak',
            field=models.IntegerField(default=0),
        ),
    ]