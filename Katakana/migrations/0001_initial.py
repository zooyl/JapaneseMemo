# Generated by Django 2.1.7 on 2019-05-14 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Katakana',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sign', models.CharField(max_length=5)),
                ('pronunciation', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Levels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preset', models.IntegerField(choices=[(0, 'Easy'), (1, 'Medium'), (2, 'Hard'), (3, 'Diacritics')])),
                ('memo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Katakana.Katakana')),
            ],
        ),
    ]