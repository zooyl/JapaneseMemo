# Generated by Django 2.1.7 on 2019-03-12 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hiragana', '0002_auto_20190312_1038'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stats',
            options={'permissions': (('medium_level', 'Can start medium level'), ('hard_level', 'Can start hard level'))},
        ),
    ]
