from django.db import models
from django.contrib.auth.models import User

# Create your models here.

level = (
    (0, 'Easy'),
    (1, 'Medium'),
    (2, 'Hard'),
)


class Stats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    completed = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)

    class Meta:
        permissions = (
            ('medium_level', "Can start medium level"),
            ('hard_level', "Can start hard level"),
            ('mixed_level', "Can start mixed level")
        )


class Hiragana(models.Model):
    sign = models.CharField(max_length=5)
    pronunciation = models.CharField(max_length=5)


class Levels(models.Model):
    preset = models.IntegerField(choices=level)
    memo = models.ForeignKey(Hiragana, on_delete=models.DO_NOTHING)
