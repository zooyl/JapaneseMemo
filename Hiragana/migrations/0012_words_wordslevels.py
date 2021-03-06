# Generated by Django 2.1.7 on 2019-05-17 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Hiragana', '0011_auto_20190514_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='Words',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('japanese_word', models.CharField(max_length=32)),
                ('meaning', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='WordsLevels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preset', models.IntegerField(choices=[(0, 'Easy'), (1, 'Medium'), (2, 'Hard'), (3, 'Diacritics')])),
                ('memo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Hiragana.Words')),
            ],
        ),
    ]
