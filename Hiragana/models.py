from django.db import models
from django.contrib.auth.models import User

# Create your models here.

level = (
    (0, 'Easy'),
    (1, 'Medium'),
    (2, 'Hard'),
    (3, 'Very Hard'),
)


class Stats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    completed = models.IntegerField(default=0)


class Hiragana(models.Model):
    sign = models.CharField()
    pronunciation = models.CharField()


class Levels(models.Model):
    memo = models.ForeignKey(Hiragana, on_delete=models.DO_NOTHING)
    preset = models.IntegerField(choices=level)
    answer = models.ForeignKey(Stats, on_delete=models.CASCADE)
